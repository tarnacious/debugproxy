import mitmproxy
from mitmproxy import http
from mitmproxy.proxy import config
import os


def respond_with_pem(flow: mitmproxy.flow.Flow, message: str="") -> None:
    filename = config.CONF_BASENAME + "-ca-cert.pem"
    p = os.path.join("~/.mitmproxy", filename)
    p = os.path.expanduser(p)
    with open(p, "rb") as f:
        certificate = f.read()

    flow.response = http.HTTPResponse.make(
        200,
        certificate,
        {
            "Content-Type": "application/x-x509-ca-cert",
            "Content-Disposition": "inline; filename={}".format(filename)
        }
    )

def respond_with_p12(flow: mitmproxy.flow.Flow, message: str="") -> None:
    filename = config.CONF_BASENAME + "-ca-cert.p12"
    p = os.path.join("~/.mitmproxy", filename)
    p = os.path.expanduser(p)
    with open(p, "rb") as f:
        certificate = f.read()

    flow.response = http.HTTPResponse.make(
        200,
        certificate,
        {
            "Content-Type": "application/x-pkcs12",
            "Content-Disposition": "inline; filename={}".format(filename)
        }
    )

def respond_with_onboarding_html(flow: mitmproxy.flow.Flow, message: str="") -> None:
    filename = config.CONF_BASENAME + "-ca-cert.p12"
    with open("proxyserver/static/onboarding.html", "rb") as f:
        html = f.read()

    flow.response = http.HTTPResponse.make(
        200,
        html,
        {
            "Content-Type": "text/html"
        }
    )
