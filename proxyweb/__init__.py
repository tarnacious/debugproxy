from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from proxyweb.startup.assets import assets
from database import init_db


app = Flask(__name__)
app.jinja_env.auto_reload = True

init_db()
assets.init_app(app)
manager = Manager(app)

from database import session

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()
