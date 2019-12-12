from flask import render_template, Blueprint
from flask import request, url_for, flash, redirect
from flask import current_app
from flask_user import current_user
from proxyweb import app
from proxyweb.views import blueprint
from flask import Blueprint
from typing import Any
from config import read_config
from database.models import ProxySession
from sqlalchemy.exc import IntegrityError
from flask_user import emails
import database as db
import requests
from email.utils import parseaddr

import os
from proxyweb.views.forms import RegisterForm
from database.models import Organization, User

config = read_config()

blueprint = Blueprint('home', __name__, url_prefix='/')
url = config["WEBSITE_URL"]

@blueprint.route('')
def home_page() -> Any:
    if current_user.is_authenticated:
        session = ProxySession.query. \
            filter(ProxySession.user_id == current_user.id).first()
        return render_template('home/index.html',
                               url=url,
                               session=session,
                               proxy_url=config["PROXYSERVER_URL"])
    else:
        return render_template('home/public.html')


@blueprint.route('about-the-beta')
def about_the_beta() -> Any:
    return render_template('home/about_the_beta.html')

@blueprint.route('certificates')
def certificates() -> Any:
    filename = os.path.join("~/.mitmproxy", "mitmproxy-ca-cert.pem")
    filename = os.path.expanduser(filename)
    with open(filename, "rb") as f:
        certificate = f.read()

    certificate = certificate.decode("utf-8").replace("\\n", "\n")
    return render_template('home/certificates.html', certificate=str(certificate))

@blueprint.route('help/android')
def android() -> Any:
    return render_template('home/android.html')

@blueprint.route('help/ios')
def ios() -> Any:
    return render_template('home/ios.html')

@blueprint.route('help/curl')
def curl() -> Any:
    return render_template('home/curl.html',
        proxy_url=config["PROXYSERVER_URL"]
    )

@blueprint.route('patternlibrary')
def patternlibrary() -> Any:
    return render_template('home/patternlibrary.html')

@blueprint.route('pricing')
def pricing() -> Any:
    return render_template('home/pricing.html')

@blueprint.route('documentation')
def documentation() -> Any:
    return render_template('home/documentation.html')

@blueprint.route('about')
def about() -> Any:
    return render_template('home/about.html')

@blueprint.route('faq')
def faq() -> Any:
    return render_template('home/faq.html')

@blueprint.route('privacy-policy')
def privacy_policy() -> Any:
    return render_template('home/privacy_policy.html')

@blueprint.route('tos')
def tos() -> Any:
    return render_template('home/tos.html')

@blueprint.route('impressum')
def impressum() -> Any:
    return render_template('home/impressum.html')

@blueprint.route('demo-videos')
def demo_videos() -> Any:
    return render_template('home/demo_videos.html')
