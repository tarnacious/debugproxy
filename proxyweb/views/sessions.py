import json
import string
import random
from flask import redirect, render_template, Blueprint, request, flash, \
    url_for, jsonify, make_response, current_app, abort, g

from flask_wtf.csrf import generate_csrf
from flask_user import login_required, current_user
from proxyweb import app
import database as db
from sqlalchemy.exc import IntegrityError
from flask import Blueprint
from proxyweb.views.forms import SessionForm, InterceptForm
from database.models import ProxySession, Request, Intercept
from sqlalchemy import desc
from sqlalchemy.orm import load_only
from flask_wtf import csrf
from typing import Any
from datetime import datetime

blueprint = Blueprint('sessions', __name__, url_prefix='/sessions/')

def random_string(size:int=5,
                  chars:str=string.ascii_lowercase) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

general_session_error = "Unable to create session. There error has been logged and we will try and resolve it as soon as possible.<br> Please try again later."
max_sessions_error = "Sorry, there are currently too many active sessions. Sessions are limited to ensure the system is not overloaded. Please try again later."
maximum_sessions = 25


@blueprint.route('generate', methods=['get'])
@login_required
def generate() -> Any:
    try:
        sessions = ProxySession.query. \
            filter(ProxySession.is_active == True). \
            count()
        if sessions >= maximum_sessions:
            app.logger.error("Maximum active sessions reached")
            flash(max_sessions_error, 'error')
            return redirect(url_for('home.home_page'))
    except:
        app.logger.exception("Exception generating session")
        flash(general_session_error, 'error')
        return redirect(url_for('home.home_page'))

    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        first()

    if not session:
        session = ProxySession()
        session.username = random_string()
        session.password = random_string()
        session.user_id = current_user.id

        try:
            db.session.add(session)
            db.session.commit()
        except IntegrityError:
            app.logger.exception("Exception generating session")
            db.session.rollback()
            flash(general_session_error, 'error')
            return redirect(url_for('home.home_page'))
        except:
            app.logger.exception("Exception generating session")
            db.session.rollback()
            flash(general_session_error, 'error')
            return redirect(url_for('home.home_page'))

    return redirect(url_for('sessions.traffic', session_id=session.id))


@blueprint.route('pause/<session_id>', methods=['get'])
@login_required
def pause(session_id) -> Any:
    try:
        session = ProxySession.query. \
            filter(ProxySession.id == session_id). \
            filter(ProxySession.user_id == current_user.id). \
            first()
        session.is_active = False
        db.session.commit()
        flash("Session paused", 'success')
    except:
        app.logger.exception("Exception pausing session")
        flash("Error pausing session", 'error')
    return redirect(url_for('home.home_page'))


@blueprint.route('enable/<session_id>', methods=['get'])
@login_required
def enable(session_id) -> Any:
    try:
        sessions = ProxySession.query. \
            filter(ProxySession.is_active == True). \
            count()
        if sessions >= maximum_sessions:
            app.logger.error("Maximum active sessions reached")
            flash(max_sessions_error, 'error')
            return redirect(url_for('home.home_page'))
    except:
        app.logger.exception("Exception generating session")
        flash(general_session_error, 'error')
        return redirect(url_for('home.home_page'))

    try:
        session = ProxySession.query. \
            filter(ProxySession.id == session_id). \
            filter(ProxySession.user_id == current_user.id). \
            first()
        session.is_active = True
        session.updated_at = datetime.now()
        db.session.commit()
        flash("Session enabled", 'success')
    except:
        app.logger.exception("Exception enabling session")
        flash("Error enabling session", 'error')
    return redirect(url_for('home.home_page'))


@blueprint.route('kill/<session_id>')
@login_required
def kill(session_id: str) -> Any:
    try:
        session = ProxySession.query. \
            filter(ProxySession.id == session_id). \
            filter(ProxySession.user_id == current_user.id). \
            first()
        db.session.delete(session)
        db.session.commit()
        flash("Session deleted", 'success')
    except:
        flash("Error deleting session", 'error')
    return redirect(url_for('home.home_page'))


@blueprint.route('delete/<session_id>')
@login_required
def delete(session_id: str) -> Any:
    try:
        session = ProxySession.query. \
            filter(ProxySession.id == session_id). \
            filter(ProxySession.user_id == current_user.id). \
            first()
        db.session.delete(session)
        db.session.commit()
        flash("Session deleted", 'success')
    except:
        flash("Error deleting session", 'error')
    return redirect(url_for('sessions.list_sessions'))


@blueprint.route('ping/<session_id>', methods=["get"])
@login_required
def ping(session_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        return jsonify({"success": False, "csrf_token": generate_csrf()})

    if not session.is_active:
        return jsonify({"success": False, "csrf_token": generate_csrf()})

    session.updated_at = datetime.now()
    db.session.commit()
    return jsonify({"success": True, "csrf_token": generate_csrf()})


@blueprint.route('traffic/<session_id>')
@login_required
def traffic(session_id: str) -> Any:
    session = ProxySession.query. \
        filter(ProxySession.user_id == current_user.id). \
        filter(ProxySession.id == session_id). \
        first()

    if not session:
        flash("Session doesn't exist", 'error')
        return redirect(url_for("home.home_page"))

    if not session.is_active:
        flash("Session is not active", 'error')
        return redirect(url_for("home.home_page"))

    requests = Request.query. \
        filter(Request.session_id == session.id). \
        order_by(desc(Request.created_at)). \
        options(load_only("state")).\
        limit(1000). \
        all()

    request_data = json.dumps(list(map(lambda x: x.state, requests)))

    proxyserver_url = current_app.config['PROXYSERVER_URL']
    proxyui_url = current_app.config['PROXYUI_URL']
    proxywebsocket_url = current_app.config['PROXYWEBSOCKET_URL']

    proxy_url = "{}:{}@{}".format(session.username,
                                  session.password,
                                  proxyserver_url)

    curl_url = 'curl debugproxy.com --proxy "{}"'.format(proxy_url)

    return render_template('sessions/traffic.html',
                           session=session,
                           proxy_url=proxy_url,
                           proxyui_url=proxyui_url,
                           websocket_url=proxywebsocket_url,
                           proxyserver_url=proxyserver_url,
                           curl_url=curl_url,
                           requests=request_data)


