import logging
logger = logging.getLogger(__name__)

from proxyworker.worker import send_websocket_message
from proxyworker.files import save_bodies

def handle_connect_ended(data, database_session):
    if "user_id" not in data or "session_id" not in data:
        logger.debug("Unidentified connection ended: {}".format(data["flow"]["id"]));
        return

    session_id = data["session_id"]
    user_id = data["user_id"]

    logger.debug("Saving connect ended to database: {}".format(data["flow"]["id"]))
    database_session.save_request(
        session_id,
        data["flow"]["id"],
        data["proxy_address"],
        data["flow"])

    logger.debug("Saving connect ended to filesystem: {}".format(data["flow"]["id"]))
    save_bodies(session_id, user_id, data)

    send_websocket_message({
        "type": "response",
        "user_id": data["user_id"],
        "session_id": data["session_id"],
        "flow": data["flow"]})
