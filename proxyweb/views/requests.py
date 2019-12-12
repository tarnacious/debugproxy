from flask import redirect, render_template, Blueprint, request, flash, \
    url_for, jsonify, make_response
from flask_user import login_required, current_user
from proxyweb import app
import database as db
from config import read_config
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from proxyweb.views.forms import SessionForm, InterceptForm
from database.models import ProxySession, Request, Intercept
from flask_wtf import csrf
from typing import Any
from proxyworker.files import read_request_body, read_response_body, save_request_body, save_response_body
import json
import base64
import gzip
from proxyweb.lib.encoding import get_header_value, get_charset, get_content_type, MultipleHeadersException

blueprint = Blueprint('requests', __name__, url_prefix='/requests/')


@blueprint.route('clear/<session_id>', methods=['POST'])
@login_required
def clear_all(session_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        return jsonify({"error": "not found"})

    Request.query. \
        filter(Request.session_id == session.id). \
        delete(synchronize_session=False)

    db.session.commit()

    return jsonify({"success": True})


@blueprint.route('response/<session_id>/<request_id>', methods=['GET', 'POST'])
@login_required
def request_response(session_id: str, request_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        return jsonify({"error": "not found"})

    request_data = Request.query. \
        filter(Request.key == request_id). \
        filter(Request.session_id == session.id). \
        first()

    if not request_data:
        return jsonify({"error": "not found"})

    user_id = current_user.id

    content_encoding = get_header_value("Content-Encoding", request_data.state["response"]["headers"])
    charset = get_charset(request_data.state["response"]["headers"])
    content_type = get_content_type(request_data.state["response"]["headers"])

    if request.method == 'POST':

        value = request.get_data()

        if charset:
            try:
                value = value.decode("utf-8")
                value = value.encode(charset)
            except:
                app.logger.exception("Error decoding body")
                return jsonify({
                    "success": False,
                    "error": "Unable to encode body",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })
        else:
            charset = "utf-8"
            encoding = "base64"
            #value = value.decode("utf-8")
            #value = base64.b64decode(value)


        if content_encoding == "gzip":
            try:
                new_value = gzip.compress(value)
                app.logger.info("Request compressed {} bytes to {} bytes".format(len(value), len(new_value)))
                value = new_value
            except:
                app.logger.exception("Error compressing gzip")
                return jsonify({
                    "success": False,
                    "error": "Unable to gzip body",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })

        save_response_body(session_id, user_id, request_id, base64.b64encode(value).decode('utf-8'))
        return jsonify({
            "success": True,
            "charset": str(charset),
            "encoding": str(content_encoding),
            "content_type": str(content_type)
         })
    else:
        body = read_response_body(session_id, user_id, request_id)
        value = base64.b64decode(body)

        if content_encoding == "gzip":
            try:
                value = gzip.decompress(value)
            except:
                return jsonify({
                    "success": False,
                    "error": "Unable to decompress",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })

        if charset:
            try:
                value = value.decode(charset)
            except:
                app.logger.exception("Error decoding body")
                return jsonify({
                    "success": False,
                    "error": "Unable to decode body",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })
        else:
            try:
                value = value.decode('iso-8859-1')
                return jsonify({
                    "success": True,
                    "response": value,
                    "charset": "iso-8859-1 (guessed)",
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                   })
            except Exception as e:
                value = base64.b64encode(value).decode('utf-8')
                return jsonify({
                    "success": True,
                    "error": "Could not guess encoding, rendering base64 encoded",
                    "response": value,
                    "charset": "base64",
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                   })

        if content_type == "application/json":
            try:
                value = json.dumps(json.loads(value),indent=4, sort_keys=True)
            except:
                pass

        return jsonify({
            "success": True,
            "response": value,
            "charset": str(charset),
            "encoding": str(content_encoding),
            "content_type": str(content_type)
           })


@blueprint.route('request/<session_id>/<request_id>', methods=['GET', 'POST'])
@login_required
def request_request(session_id: str, request_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        return jsonify({"error": "not found"})

    request_data = Request.query. \
        filter(Request.key == request_id). \
        filter(Request.session_id == session.id). \
        first()

    user_id = current_user.id

    if not request_data:
        return jsonify({"error": "not found"})

    content_encoding = get_header_value("Content-Encoding", request_data.state["request"]["headers"])
    charset = get_charset(request_data.state["request"]["headers"])
    content_type = get_content_type(request_data.state["request"]["headers"])

    if request.method == 'POST':
        data = base64.b64encode(request.get_data()).decode("utf-8")
        save_request_body(session_id, user_id, request_id, data)
        return jsonify({"success": True})
    else:
        value = ""
        body = read_request_body(session_id, user_id, request_id)
        value = base64.b64decode(body)

        if content_encoding == "gzip":
            try:
                value = gzip.decompress(value)
            except:
                return jsonify({
                    "success": False,
                    "error": "Unable to decompress",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })

        if charset:
            try:
                value = value.decode(charset)
                return jsonify({
                    "success": True,
                    "response": value,
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                   })
            except:
                app.logger.exception("Error decoding body")
                return jsonify({
                    "success": False,
                    "error": "Unable to decode body",
                    "charset": str(charset),
                    "encoding": str(content_encoding),
                    "content_type": str(content_type)
                 })

        try:
            value = value.decode('utf-8')
            return jsonify({
                "success": True,
                "response": value,
                "charset": "utf-8",
                "encoding": str(content_encoding),
                "content_type": str(content_type)
               })
        except:
            return jsonify({
                "success": False,
                "error": "Unable to decode body",
                "charset": str(charset),
                "encoding": str(content_encoding),
                "content_type": str(content_type)
             })


@blueprint.route('state/<session_id>/<request_id>', methods=['GET', 'POST'])
@login_required
def request_state(session_id: str, request_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        return jsonify({"error": "not found"})

    request_data = Request.query. \
        filter(Request.key == request_id). \
        filter(Request.session_id == session.id). \
        first()

    if not request:
        return jsonify({"error": "not found"})

    if request.method == 'POST':
        request_data.state = json.loads(request.get_data().decode())
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify(request_data.state)
