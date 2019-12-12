import mitmproxy
from base64 import b64decode
from typing import List, Set, Dict, Tuple, Text, Optional
from mitmproxy import http
import logging

logger = logging.getLogger(__name__)

def is_authorization_header(header):
    name, value = header
    return name.lower() == "proxy-authorization"

def encode_header(header):
    name, value = header
    return (name.encode(), value.encode())

def parse_proxy_authentication_headers(header: str) -> Optional[Tuple[str, str]]:
    auth_data = b64decode(header.split(" ")[1]).decode(encoding='UTF-8')
    parts = auth_data.split(":")
    if len(parts) != 2:
        return None
    (user, password) = parts
    return (user, password)

def get_case_insensitive_key_value(input_dict, key):
    return next((value for dict_key, value in input_dict.items() if dict_key.lower() == key.lower()), None)

def get_credentials(flow: mitmproxy.flow.Flow):
    request = flow["request"]
    headers = request["headers"]
    headers = dict(headers).get("Proxy-Authorization")

    if not headers:
        # Check for case insensitive header
        headers = get_case_insensitive_key_value(dict(request["headers"]), "Proxy-Authorization")

    if not headers:
        # no auth header
        return None

    authentication = parse_proxy_authentication_headers(headers)
    return authentication

def authorize(flow: mitmproxy.flow.Flow, database_session) -> Optional[Tuple[str, str]]:

    credentials = get_credentials(flow)

    if not credentials:
        return None

    (username, password) = credentials
    session = database_session.get_session_and_user_id(username, password)

    return session
