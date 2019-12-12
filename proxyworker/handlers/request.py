import logging
import json
logger = logging.getLogger(__name__)

from proxyworker.worker import loop
from proxyworker.worker import redis_pool
from proxyworker.worker import send_websocket_message
from proxyworker.worker import send_proxy_message

from proxyworker.authorize import authorize, get_credentials
from proxyworker.intercept_matching import intercept_request
from proxyworker.ratelimiting import check_ratelimit
from proxyserver.redis import increment_counter
from proxyworker.files import save_bodies


def handle_request(data, database_session):
    flow_id = data["flow"]["id"]
    server = data["proxy_address"]

    session = None
    try:

        # HTTPS request are already authenticated
        if data.get("user_id") and data.get("session_id"):
            logger.debug("Flow already authorized: {}".format(flow_id))
            session = (data["session_id"], data["user_id"])

            # HTTPS requests are still ratelimited
            key = "{}-{}".format(data.get("user_id"), data.get("session_id"))
            if not check_ratelimit(key):
                loop.run_until_complete(
                        increment_counter(redis_pool, "rate_limited")
                        )


                flow = data["flow"]
                flow["error"] = {"msg": "Proxy ratelimit exceeded, please slow down."}
                flow["intercepted"] = False
                send_websocket_message({
                    "type": "request",
                    "user_id": data.get("user_id"),
                    "session_id": data.get("session_id"),
                    "flow": flow})

                logger.info("Flow not authorized, rate limited exceeded: {}".format(flow_id))
                data = json.dumps({"type": "rate-limit-exceeded",
                                   "flow": data["flow"]})
                send_proxy_message(server, data)
                return
        else:
            credentials = get_credentials(data["flow"])

            if credentials:
                key = "-".join(credentials)
                if (check_ratelimit(key)):
                    session = authorize(data["flow"], database_session)
                else:
                    loop.run_until_complete(
                        increment_counter(redis_pool, "rate_limited")
                    )

                    session = authorize(data["flow"], database_session)
                    if session:
                        (session_id, user_id) = session
                        flow = data["flow"]
                        flow["error"] = {"msg": "Proxy ratelimit exceeded, please slow down."}
                        flow["intercepted"] = False

                        send_websocket_message({
                            "type": "request",
                            "user_id": user_id,
                            "session_id": session_id,
                            "flow": flow})

                    logger.info("Flow not authorized, rate limited exceeded: {}".format(flow_id))
                    data = json.dumps({"type": "rate-limit-exceeded",
                                       "flow": data["flow"]})
                    send_proxy_message(server, data)
                    return

        if not session:
            loop.run_until_complete(
                increment_counter(redis_pool, "not_authorized")
            )
            logger.debug("Flow not authorized, no session: {}".format(flow_id))
            data = json.dumps({"type": "not-authorized",
                               "flow": data["flow"]})
            send_proxy_message(server, data)
            return

        loop.run_until_complete(
            increment_counter(redis_pool, "authorized")
        )

        (session_id, user_id) = session

        logger.debug("Saving request to database: {}".format(data["flow"]["id"]))
        database_session.save_request(
            session_id,
            data["flow"]["id"],
            server,
            data["flow"])


        logger.debug("Saving request to filesystem: {}".format(data["flow"]["id"]))
        save_bodies(session_id, user_id, data)

        intercept = intercept_request(data, session_id, database_session)

        if (intercept):

            loop.run_until_complete(
                increment_counter(redis_pool, "intercepted")
            )

            logger.info("Flow matches intercept rule: {}".format(data["flow"]["id"]))
            data["flow"]["intercepted"] = True
            message = {
                "type": "intercept",
                "user_id": user_id,
                "session_id": session_id,
                "flow": data["flow"]
            }
            send_proxy_message(server, json.dumps(message))

            send_websocket_message(message)
            return


        logger.debug("Sending message to websocket: {}".format(data["flow"]["id"]))
        data["flow"]["intercepted"] = False

        send_websocket_message({
            "type": "request",
            "user_id": user_id,
            "session_id": session_id,
            "flow": data["flow"]})

        proxy_server_message = json.dumps({
            "type": "resume",
            "user_id": user_id,
            "session_id": session_id,
            "flow": data["flow"]})

        logger.debug("Sending message to proxyserver: {}".format(data["flow"]["id"]))
        send_proxy_message(server, proxy_server_message)
    except:
        logger.exception("Error handling request: {}".format(data["flow"]["id"]))
        proxy_server_message = json.dumps({
            "type": "worker-error",
            "flow": data["flow"]})
        logger.debug("Sending error message to proxyserver: {}".format(data["flow"]["id"]))
        send_proxy_message(server, proxy_server_message)
