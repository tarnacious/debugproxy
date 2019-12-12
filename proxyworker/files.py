import pathlib
from config import read_config
config = read_config()
data_path = config["DATA_PATH"]

def save_bodies(session_id, user_id, data):
    session_path = '{}/{}/{}'.format(data_path, user_id, session_id)
    pathlib.Path(session_path).mkdir(parents=True, exist_ok=True)
    flow_id = data["flow"]["id"]

    request_data = data.get("request")
    if request_data:
        save_request_body(session_id, user_id, flow_id, request_data)

    response_data = data.get("response")
    if response_data:
        save_response_body(session_id, user_id, flow_id, response_data)


def save_request_body(session_id, user_id, flow_id, data):
    session_path = '{}/{}/{}'.format(data_path, user_id, session_id)
    pathlib.Path(session_path).mkdir(parents=True, exist_ok=True)

    binary_data = data.encode("utf-8")
    with open("{}/{}.request".format(session_path, flow_id), 'wb') as f:
        f.write(binary_data)


def save_response_body(session_id, user_id, flow_id, data):
    session_path = '{}/{}/{}'.format(data_path, user_id, session_id)
    pathlib.Path(session_path).mkdir(parents=True, exist_ok=True)

    binary_data = data.encode("utf-8")
    with open("{}/{}.response".format(session_path, flow_id), 'wb') as f:
        f.write(binary_data)


def read_request_body(session_id, user_id, flow_id):
    session_path = '{}/{}/{}/{}.request'.format(data_path, user_id, session_id, flow_id)
    print(session_path)
    if pathlib.Path(session_path).is_file():
        with open(session_path, "rb") as f:
            return f.read().decode("utf-8")
    return ""

def read_response_body(session_id, user_id, flow_id):
    session_path = '{}/{}/{}/{}.response'.format(data_path, user_id, session_id, flow_id)
    print(session_path)
    if pathlib.Path(session_path).is_file():
        with open(session_path, "rb") as f:
            return f.read().decode("utf-8")
    return ""
