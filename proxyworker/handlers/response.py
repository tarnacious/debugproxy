import logging
import json
logger = logging.getLogger(__name__)

from proxyworker.worker import send_websocket_message
from proxyworker.files import save_bodies


def handle_response(data, database_session):
    flow_id = data["flow"]["id"]
    session_id = data["session_id"]
    user_id = data["user_id"]
    flow = data["flow"]

    logger.debug("Saving response to database: {}".format(flow_id))

    database_session.update_request(
        session_id,
        flow_id,
        flow)

    logger.debug("Saving request to filesystem: {}".format(flow_id))
    save_bodies(session_id, user_id, data)

    send_websocket_message({
        "type": "response",
        "user_id": user_id,
        "session_id": session_id,
        "flow": flow})



