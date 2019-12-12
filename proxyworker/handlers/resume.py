import logging
import json
logger = logging.getLogger(__name__)

from proxyworker.worker import send_proxy_message
from proxyworker.files import read_request_body, read_response_body


def handle_resume(data, database_session):
    logger.info("Fetching request to resume: {}".format(data["flow"]["id"]));

    session_id = data["session_id"]
    user_id = data["user_id"]
    flow_id = data["flow"]["id"]

    request = database_session.get_request(flow_id)

    request_data = read_request_body(session_id, user_id, flow_id)
    response_data = read_response_body(session_id, user_id, flow_id)

    if request:
        logger.info("Request to resume found in database: {}".format(data["flow"]["id"]));
        message = {
            "id": flow_id,
            "type": "user_resume",
            "user_id": user_id,
            "session_id": session_id,
            "flow": request.state,
            "request_data": request_data,
            "response_data": response_data
        }

        send_proxy_message(request.proxyserver, json.dumps(message))
        logger.info("Resume sent to proxyserver: {}".format(data["flow"]["id"]));
    else:
        logger.error("No request to resume found in database: {}".format(data["flow"]["id"]));
