import logging
from mitmproxy import http
import mitmproxy
import json
import base64

from proxyserver.status_codes import status_code_reason
from mitmproxy.exceptions import TlsProtocolException
from mitmproxy.proxy.protocol import TlsLayer, RawTCPLayer
from proxyserver.intercept import Intercept
from proxyserver.connection import Connection
from datetime import datetime
from typing import List, Set, Dict, Tuple, Text, Optional
from mitmproxy import ctx
from mitmproxy.script import concurrent
from base64 import b64encode
from mitmproxy.net.http.headers import Headers
from proxyserver import certificates
from proxyworker.authorize import is_authorization_header, encode_header
from proxyserver.connection import Connection
from proxyserver.redis import increment_counter, subscription_reader, subscribe_to_channel
from proxyserver.message_handler import handle_message
import asyncio

from proxyserver.errors import (
    respond_with_forbidden,
    respond_with_auth_failure,
    respond_with_rate_limit_failure,
    respond_with_server_error
)

from config import read_config
config = read_config()
logger = logging.getLogger(__name__)


class Proxy:
    def __init__(self, messenger, redis_pool, loop) -> None:
        self.messenger = messenger
        self.loop = loop
        self.redis_pool = redis_pool
        self.connections = dict() # type: Dict[str, Connection]
        self.intercepts = dict() # type: Dict[str, Intercept]

    def handle_message(self, message):
        handle_message(message, self)

    async def subscribe_to_queue(self):
        logger.info("Subscribe to redis pub/sub queue")
        try:
            subscriber = await subscribe_to_channel(self.loop, self.redis_pool)
            asyncio.ensure_future(subscription_reader(subscriber, self))
        except Exception as e:
            logger.info("Error subscribing to queue", e)
            await asyncio.sleep(5)
            await self.subscribe_to_queue()

    def worker_error(self, message, desc = "unable to queue request"):
        logger.info("Worker error.")
        try:
            flow_id = message["flow"]["id"]
            logger.info("intercept count: {}".format(len(self.intercepts)))
            logger.info("connect count: {}".format(len(self.connections)))
            intercept = self.intercepts.get(flow_id, None)
            if intercept:
                logger.info("respond with worker error: {}".format(flow_id))
                intercept.flow.resume()
                intercept.rejected = True
                respond_with_server_error(intercept.flow, "Proxy error")
            else:
                logger.info("no intercept found: {}".format(flow_id))

            connection = self.connections.get(message["flow"]["client_conn"]["id"], None)
            if connection:
                logger.info("respond with worker error: {}".format(flow_id))
                respond_with_server_error(connection.flow, "debugProxy error: {}.".format(desc))
                connection.flow.resume()
            else:
                logger.info("no connection found: {}".format(flow_id))
        except:
            logger.exception("Error handling worker error")

    def send_message(self, message_type, intercept):
        self.messenger.send_message(message_type, intercept, self)

    def authorize_connect(self, data):
        """
        Message from worker indicating it has authorized a connect request. It
        should include a user_id and a session_id.

        Here the meta information about the intercept is updated.
        """
        connection = self.connections.get(data["flow"]["client_conn"]["id"], None)
        if not connection:
            logger.info("Unable to authorize connect, not found. ({}, {}) {}".format(
                data["flow"]["client_conn"]["id"],
                data["flow"]["id"]
            ))
            return

        user_id = data.get("user_id")
        session_id = data.get("session_id")
        if user_id and session_id:
            logger.info("Authorizing connect ({}, {}) {}".format(
                user_id,
                session_id,
                connection.flow.id))
            connection.user_id = user_id
            connection.session_id = session_id
        else:
            logger.info("Unable to authorize connect ({}, {}) {}".format(
                user_id,
                session_id,
                data["flow"]["id"]))

        # Resume the flow regardless if it is authorized or now. With or without
        # authorization it will get handled correctly later.
        logger.debug("Resuming connect. ({}, {})".format(
            data["flow"]["client_conn"]["id"],
            data["flow"]["id"]
        ))
        connection.flow.resume()


    def authorize(self, data):
        """
        Message from worker indicating it has authorized the request. It should
        include a user_id and a session_id.

        Here the meta information about the intercept is updated.
        """
        intercept = self.intercepts.get(data["flow"]["id"], None)
        user_id = data.get("user_id")
        session_id = data.get("session_id")
        if intercept and user_id and session_id:
            logger.info("Authorizing request ({}, {}) {}".format(
                user_id,
                session_id,
                intercept.flow.id))
            intercept.user_id = user_id
            intercept.session_id = session_id
            intercept.connection.user_id = user_id
            intercept.connection.session_id = session_id
        else:
            logger.info("Unable to authorize request ({}, {}) {}".format(
                user_id,
                session_id,
                data["flow"]["id"]))


    def not_authorized(self, data) -> None:
        """
        Message from worker indicating it has not authorized the request.

        The flows response is set to an error and it is resumed.
        """
        logger.debug("Not authorized handler".format(data["id"]))
        intercept = self.intercepts.get(data["id"], None)
        if intercept:
            logger.info("Responding with auth failure {}".format(data["id"]))
            intercept.flow.resume()
            respond_with_auth_failure(intercept.flow)
            intercept.rejected = True
        else:
            connection = self.connections.get(data["client_conn"]["id"],
                                              None)
            if connection:
                logger.info("Respond to connect with auth failure {}".format(data["id"]))
                connection.flow.resume()
                # Don't response with auth failure for connect, but let furthur requests fail
                #respond_with_auth_failure(connection.flow)
            else:
                logger.info("No flow found to reject".format(data["id"]))


    def rate_limit_exceeded(self, data):
        """
        Message from worker indicating it has not authorized the request.

        The flows response is set to an error and it is resumed.
        """
        logger.debug("Rate limited exceeded handler".format(data["id"]))

        intercept = self.intercepts.get(data["id"], None)
        if intercept:
            logger.info("Responding with rate limit failure {}".format(data["id"]))
            intercept.flow.resume()
            respond_with_rate_limit_failure(intercept.flow)
            intercept.rejected = True
            return

        connection = self.connection.get(data["client_conn"]["id"], None)
        if connection:
            logger.info("Responding connect with rate limit failure {}".format(data["id"]))
            connection.flow.resume()
            respond_with_rate_limit_failure(connection.flow)
            return

        logger.info("No flow found to reject".format(data["id"]))


    def user_intercept(self, id):
        intercept = self.intercepts.get(id, None)
        if intercept:
            logger.info("User intercept request: {}".format(
                intercept.flow.id))
            intercept.intercepted = True
        else:
            logger.info("Unable to find user intercept request {}".format(
                intercept.flow.id))


    def user_resume(self, data: dict) -> None:
        """
        Handle a message signaling that the request should be resumed. The
        messages includes a request and possibly a response. It may have been
        modified.

        The flow needs be found in the intercept dictionary, then it should be
        updated with any updated data we have before it is resumed.

        If the flow is in the response stage, it should be removed from the our
        intercepts dictionary as we have no need to find it again.
        """
        logger.debug("User Resume")
        flow_id = data.get("id")
        if not flow_id:
            logger.info("Ignoring user intercept with no id")
            return

        user_id = data.get("user_id")
        session_id = data.get("session_id")
        if not user_id and not session_id:
            logger.info("Ignoring user intercept with no credentials")
            return

        intercept = self.intercepts.get(flow_id, None)
        if not intercept:
            logger.info("User intercept not found {}".format(flow_id))
            return

        if str(intercept.user_id) != str(user_id) or str(intercept.session_id) != str(session_id):
            logger.info("User intercept credentials incorrect. Got ({}, {}). Expected ({}, {}) {}".format(
                user_id, session_id,
                intercept.user_id, intercept.session_id,
                flow_id
            ))
            return

        if not intercept.flow.response:
            logger.info("User resuming request %s" % intercept.flow.id)
            intercept.flow.request.host = data["flow"]["request"]["host"]
            intercept.flow.request.scheme = data["flow"]["request"]["scheme"]
            intercept.flow.request.path = data["flow"]["request"]["path"]
            intercept.flow.request.port = data["flow"]["request"]["port"]
            intercept.flow.request.method = data["flow"]["request"]["method"]

            headers = data["flow"]["request"]["headers"]
            intercept.flow.request.headers = Headers(list(map(encode_header,
                                                              headers)))

            intercept.flow.request.raw_content = base64.b64decode(data["request_data"])


            intercept.flow.resume()
        else:
            logger.info("User resuming response %s" % intercept.flow.id)

            try:
                status_code = int(data["flow"]["response"]["status_code"])
                if 100 <= status_code <= 599:
                    intercept.flow.response.status_code = status_code
                    intercept.flow.response.reason = status_code_reason(status_code)
                else:
                    logger.error("Status code code out of range: {}".format(status_code))
            except:
                logger.exception("Error setting status_code")



            headers = data["flow"]["response"]["headers"]
            intercept.flow.response.headers = Headers(list(map(encode_header,
                                                               headers)))

            intercept.flow.response.raw_content = base64.b64decode(data["response_data"])
            if "Content-Length" in intercept.flow.response.headers:
                print("has length")
                header_length = intercept.flow.response.headers.get("Content-Length")
                real_length = len(intercept.flow.response.raw_content)
                if (header_length != real_length):
                    logger.error("Body size doesn't match Content-Length %s" % intercept.flow.id)
                    logger.warning("Setting Content-Length %s" % intercept.flow.id)
                    intercept.flow.response.headers["Content-Length"] = str(real_length)
            else:
                print("no content length")

            intercept.flow.resume()
            del self.intercepts[intercept.flow.id]
            logger.info("Removing response: {}".format(intercept.flow.id))


    def resume(self, id: str) -> None:
        logger.debug("Resume {}".format(id))
        intercept = self.intercepts.get(id, None)
        if intercept:
            url = config["WEBSITE_URL"]
            if intercept.flow.request.url == '{}/certificates/p12'.format(url):
                logger.info("Download p12 certificate: {}".format(id))
                certificates.respond_with_p12(intercept.flow)
                intercept.flow.resume()
                return

            if intercept.flow.request.url == '{}/certificates/pem'.format(url):
                logger.info("Download pem certificate: {}".format(id))
                certificates.respond_with_pem(intercept.flow)
                intercept.flow.resume()
                return

            if intercept.flow.request.url == '{}/certificates'.format(url):
                logger.info("Download onboarding certificate: {}".format(id))
                certificates.respond_with_onboarding_html(intercept.flow)
                intercept.flow.resume()
                return

            if not intercept.modified:
                logger.debug("Resuming request {}".format(intercept.flow.id))
                intercept.flow.resume()
                return

            if not intercept.flow.response:
                logger.debug("Resuming request %s" % intercept.flow.id)
                intercept.flow.resume()
                return

            logger.debug("Resuming response %s" % intercept.flow.id)
            intercept.flow.resume()
            # TODO: move this to response handler?
            del self.intercepts[id]
        else:
            logger.warning("No flow found {}".format(id))


    def intercept_timeout(self, id: str) -> None:
        logger = logging.getLogger()
        try:
            logger.info("Resuming intercept after timeout: %s" % id)
            intercept = self.intercepts[id]
            intercept.flow.resume()
            self.send_message("intercept_timeout", intercept);
            del self.intercepts[id]
        except Exception as e:
            logger.exception("Error resuming intercept after timeout. %s" % id)


    def clientdisconnect(self, connection):
        try:
            logger.debug("client disconnected {}" \
                         .format(connection.ctx.client_conn.id))

            conn = self.connections.get(connection.ctx.client_conn.id)
            if (conn):

                # delete child requests
                for key, value in conn.requests.items():
                    intercept = self.intercepts.get(key)
                    if (intercept):
                        logger.debug("disconnect: request deleted {}" \
                                   .format(key))
                        del self.intercepts[key]

                # update worker that a connection is ended
                self.send_message("connect-ended", conn);

                # delect connection itself
                logger.debug("disconnect: connection deleted {}" \
                             .format(connection.ctx.client_conn.id))
                del self.connections[connection.ctx.client_conn.id]

            else:
                logger.warning("disconnect: connection not found")
        except:
            logger.exception("client disconnection handling error. %s" \
                             .format(connection.client_conn.id))


    def error(self, flow: mitmproxy.flow.Flow):
        """
        Handle error event raised by mitmproxy.

        If an intercept is found for the flow, a message is sent to a worker and
        the intercept is removed.

        An error is return to the client.
        """
        try:
            logger.debug("Error {} {}".format(flow.error, flow.id))

            self.loop.create_task(
                increment_counter(self.redis_pool, "errors"))

            intercept = self.intercepts.get(flow.id)
            if intercept:
                logger.debug("Sending request error message to worker {}".format(flow.id))
                self.send_message("error", intercept);
                logger.debug("Removign intercept {}".format(flow.id))
                del self.intercepts[flow.id]

            connections = self.connections.get(flow.client_conn.id)
            if connections:
                logger.debug("Sending connect error message to worker {}".format(flow.id))
                self.send_message("connect-ended", connections);
                logger.debug("Removign connection {}".format(flow.id))
                del self.connections[flow.client_conn.id]

            logger.debug("Respond with server error {}".format(flow.id))
            respond_with_server_error(flow, message="Sever error")
        except:
            logger.exception("Exception handling error. %s" % id)


    def http_connect(self, flow):
        """
        Handle TLS connect.
        """
        try:
            logger.info("{} {} {} {}".format(flow.request.method,
                                             flow.request.pretty_url,
                                             flow.id,
                                             flow.client_conn.id))

            self.loop.create_task(
                increment_counter(self.redis_pool, "connects"))

            connection = Connection(flow)
            self.connections[flow.client_conn.id] = connection
            flow.intercept()
            self.send_message("connect", connection);
        except Exception as e:
            logger.exception("Exception handling HTTP connect: ", flow.id)


    def request(self, flow: mitmproxy.flow.Flow) -> None:
        """
        Handle request event from mitmproxy. We intercept the request to prevent
        further action by mitmproxy, add it to our dictionary of intercepts and
        send the request to the workers to be authorized.
        """
        try:
            logger.debug("request handler id: {}".format(flow.client_conn.id))
            logger.info("{} {} ({})".format(flow.request.method,
                                            flow.request.url,
                                            flow.id))


            self.loop.create_task(
                increment_counter(self.redis_pool, "requests"))


            flow.intercept()

            # handle authorized connection
            connection = self.connections.get(flow.client_conn.id)
            if (connection):
                intercept = Intercept(flow, connection)
                intercept.session_id = connection.session_id
                intercept.user_id = connection.user_id
                connection.requests[flow.id] = intercept
                self.intercepts[flow.id] = intercept
                self.send_message("request", intercept);
                return

            connection = Connection(flow)
            intercept = Intercept(flow, connection)
            connection.requests[flow.id] = intercept
            self.connections[flow.client_conn.id] = connection
            self.intercepts[flow.id] = intercept

            self.send_message("request", intercept);

            # remove proxy authentication headers
            headers = list(flow.request.headers.items())
            clean = filter(lambda h: not is_authorization_header(h), headers)
            flow.request.headers = Headers(list(map(encode_header, clean)))



        except Exception as e:
            logger.exception("Exception handling request: ", flow.id)


    def response(self, flow: mitmproxy.flow.Flow) -> None:
        """
        Handle response event from mitmproxy
        """
        try:
            logger.debug("Response Handler: {}".format(flow.id))

            self.loop.create_task(
                increment_counter(self.redis_pool, "responses"))

            intercept = self.intercepts.get(flow.id)
            if intercept:

                if intercept.rejected:
                    logger.debug("Removing rejcted intercept: {}".format(flow.id))
                    del self.intercepts[intercept.flow.id]
                    return

                if not intercept.user_id and not intercept.session_id:
                    logger.info("Return auth failure: {}".format(flow.id))
                    logger.info("HTTPS Response: {}".format(flow.response))
                    respond_with_auth_failure(intercept.flow)
                    return

                if not intercept.intercepted:
                    logger.info("Return response to client: {} {}".format(
                        flow.request.url,
                        flow.id))
                    self.send_message("response", intercept);
                    return
                else:
                    intercept.flow.intercept()
                    self.send_message("intercept", intercept);
                    return
            else:
                logger.error("No intercept found for response, respond with server error: {}".format(flow.id))
                respond_with_server_error(flow, "debugProxy error: timeout waiting for request update")
        except Exception as e:
            logger.exception("Exception handling response")
            respond_with_server_error(flow, "debugProxy error: error handling response")

