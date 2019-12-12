import logging
import json
import pathlib
logger = logging.getLogger(__name__)

from proxyworker.worker import send_websocket_message, send_proxy_message

from proxyworker.authorize import authorize
from proxyworker.intercept_matching import intercept_request
from proxyworker.ratelimiting import check_ratelimit
from proxyserver.redis import increment_counter
from proxyworker.files import save_bodies


def handle_connect(data, database_session):
    flow_id = data["flow"]["id"]
    server = data["proxy_address"]

    try:
        session = authorize(data["flow"], database_session)

        if not session:
            logger.debug("Not authorized: {}".format(flow_id))
            data = json.dumps({"type": "not-authorized",
                               "flow": data["flow"]})
            logger.debug("Updated proxy server: not-authorized, {}".format(flow_id))
            send_proxy_message(server, data)
            return

        (session_id, user_id) = session

        logger.debug("Sending message to websocket")
        data["flow"]["intercepted"] = False


        logger.debug("Saving connect to database: {}".format(data["flow"]["id"]))
        database_session.save_request(
            session_id,
            data["flow"]["id"],
            server,
            data["flow"])

        logger.debug("Saving connect to filesystem: {}".format(data["flow"]["id"]))
        save_bodies(session_id, user_id, data)

        send_websocket_message({
            "type": "connect",
            "user_id": user_id,
            "session_id": session_id,
            "flow": data["flow"]})

        resume_connect_message = json.dumps({
            "type": "resume_connect",
            "user_id": user_id,
            "session_id": session_id,
            "flow": data["flow"]})

        logger.info("Sending resume_connect message to proxy: {}".format(data["flow"]["id"]))
        send_proxy_message(server, resume_connect_message)
    except:
        logger.exception("Exception handling connect: {}".format(data["flow"]["id"]))
        logger.info("Sending worker-error message to proxy: {}".format(data["flow"]["id"]))
        try:
            message_data = json.dumps({
                "type": "worker-error",
                "flow": data["flow"]})
            send_proxy_message(server, message_data)
        except:
            logger.exception("Exception sending worker-error message to proxy: {}".format(data["flow"]["id"]))

