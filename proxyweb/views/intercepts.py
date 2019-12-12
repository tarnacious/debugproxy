from flask import redirect, render_template, Blueprint, request, flash, \
    url_for, jsonify, make_response, abort
from flask_user import login_required, current_user
from proxyweb import app
import database as db
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from proxyweb.views.forms import SessionForm, InterceptForm
from database.models import ProxySession, Request, Intercept
from flask_wtf import csrf
from typing import Any
import json

blueprint = Blueprint('intercepts', __name__, url_prefix='/intercepts/')

def intercept_to_dict(intercept):
    return {
        "id": intercept.id,
        "query": intercept.query
    }

@blueprint.route('all/<session_id>')
@login_required
def all(session_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.id == session_id). \
        filter(ProxySession.user_id == current_user.id). \
        first()

    if not session:
        abort(404);

    intercepts = db.session.query(Intercept). \
        filter(Intercept.session_id == session_id). \
        all()

    result = [intercept_to_dict(intercept) for intercept in intercepts]

    return jsonify({ "intercepts": result});


@blueprint.route('update/<session_id>/<intercept_id>', methods=['POST'])
@login_required
def update(session_id: str, intercept_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.id == session_id). \
        filter(ProxySession.user_id == current_user.id). \
        first()

    if not session:
        abort(404);

    intercept = db.session.query(Intercept). \
        filter(Intercept.session_id == session_id). \
        filter(Intercept.id == intercept_id). \
        first()

    if not intercept:
        abort(404);

    updated = json.loads(request.get_data().decode('utf-8'))
    intercept.query = updated["query"]
    db.session.commit()

    return jsonify({"success": True})


@blueprint.route('create/<session_id>', methods=['POST'])
@login_required
def api_create(session_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.id == session_id). \
        filter(ProxySession.user_id == current_user.id). \
        first()

    if not session:
        abort(404);

    intercepts = db.session.query(Intercept). \
        filter(Intercept.session_id == session_id). \
        count()

    if intercepts > 2:
        return jsonify({
            "success": False,
            "message": "Too many intercepts for a session"
        })

    updated = json.loads(request.get_data().decode('utf-8'))
    intercept = Intercept()
    intercept.session_id = session_id
    intercept.query = updated["query"]
    intercept.method = ""
    db.session.add(intercept)
    db.session.commit()

    return jsonify({
        "success": True,
        "intercept": intercept_to_dict(intercept)
    })


@blueprint.route('delete/<session_id>/<intercept_id>', methods=['POST'])
@login_required
def api_delete(session_id: str, intercept_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.id == session_id). \
        filter(ProxySession.user_id == current_user.id). \
        first()

    if not session:
        abort(404);

    intercept = db.session.query(Intercept). \
        filter(Intercept.session_id == session_id). \
        filter(Intercept.id == intercept_id). \
        first()

    if not intercept:
        abort(404);

    db.session.delete(intercept)
    db.session.commit()

    return jsonify({"success": True})
