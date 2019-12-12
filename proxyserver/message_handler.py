import logging
import json

logger = logging.getLogger(__name__)

def handle_message(message, proxy):
    try:
        data = json.loads(message.decode('utf-8'))
        flow = data.get("flow")
        if flow:
            flow_id = flow["id"]
        else:
            flow_id = None

        logger.debug("Worker message {} {}".format(data.get("type"), flow_id))
        if data.get("type") == "user_resume":
            proxy.user_resume(data)
        elif data.get("type") == "resume":
            proxy.authorize(data)
            proxy.resume(flow["id"])
        elif data.get("type") == "intercept":
            proxy.authorize(data)
            proxy.user_intercept(flow["id"])
        elif data.get("type") == "not-authorized":
            proxy.not_authorized(flow)
        elif data.get("type") == "rate-limit-exceeded":
            proxy.rate_limit_exceeded(flow)
        elif data.get("type") == "resume_connect":
            proxy.authorize_connect(data)
        elif data.get("type") == "closing-channel":
            #proxy.subscribe_to_queue()
            pass
        elif data.get("type") == "worker-error":
            proxy.worker_error(data, "processing request")
            pass
        else:
            if flow_id:
                logger.error(
                    "Unknown action {}, resuming {}".format(data.get("type"), flow_id))
                proxy.resume(flow_id)
            else:
                logger.error(
                    "Unknown action, no flow. {}".format(data.get("type")))
    except Exception as e:
        logger.exception("Exception worker message");
