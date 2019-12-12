import mitmproxy
from mitmproxy import http


def respond_with_forbidden(flow: mitmproxy.flow.Flow,
                           message: str="") -> None:

    flow.response = http.HTTPResponse.make(
        403,
        b"Address must be global",
        {"Content-Type": "text/html",
         "Proxy-Authenticate": "BASIC"}
    )


def respond_with_auth_failure(flow: mitmproxy.flow.Flow,
                              message: str="") -> None:
    flow.response = http.HTTPResponse.make(
        407,
        b"Proxy-Authorization required",
        {"Content-Type": "text/html",
            "Proxy-Authenticate": "BASIC"}
    )


def respond_with_server_error(flow: mitmproxy.flow.Flow,
                              message: str="") -> None:
    flow.response = http.HTTPResponse.make(
        500,
        message,
        {"Content-Type": "text/plain" }
    )


def respond_with_rate_limit_failure(flow: mitmproxy.flow.Flow,
                                    message: str="") -> None:
    flow.response = http.HTTPResponse.make(
        429,
        "Too Many Requests",
        {"Content-Type": "text/html",
         "Proxy-Authenticate": "BASIC"}
    )
