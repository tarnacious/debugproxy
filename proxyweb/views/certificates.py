from flask import make_response, Blueprint
from flask_user import login_required
from proxyweb.views import blueprint
import os

blueprint = Blueprint('certificates', __name__, url_prefix='/certificates/')

@blueprint.route('pem', methods=['GET', 'POST'])
def pem():
    filename = os.path.join("~/.mitmproxy", "mitmproxy-ca-cert.pem")
    filename = os.path.expanduser(filename)
    with open(filename, "rb") as f:
        certificate = f.read()
    response = make_response(certificate, 200)

    response.headers["Content-Type"] = "application/x-x509-ca-cert"
    response.headers["Content-Disposition"] = "inline; filename=ca-cert.pem"
    return response

@blueprint.route('p12', methods=['GET', 'POST'])
def p12():
    filename = os.path.join("~/.mitmproxy", "mitmproxy-ca-cert.p12")
    filename = os.path.expanduser(filename)
    with open(filename, "rb") as f:
        certificate = f.read()
    response = make_response(certificate, 200)

    response.headers["Content-Type"] = "application/application/x-pkcs12"
    response.headers["Content-Disposition"] = "inline; filename=ca-cert.p12"
    return response
