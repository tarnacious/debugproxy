# *****************************
# Environment specific settings
# *****************************

# Flask settings
SECRET_KEY = 'een3Teinigh4BeeYaesh4ahtegheejei5Ooyeipeingi4thaho' # type: str

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/website' # type: str

DATA_PATH = "./data"

# Flask-Mail settings
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
USER_EMAIL_SENDER_NAME = ''
USER_EMAIL_SENDER_EMAIL = ''
MAIL_SERVER = ''
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True

LOG_FILE = '/tmp/website.log'

REDIS_HOST = "localhost"
REDIS_PORT = "6379"

# Script / server urls
PROXYUI_URL = 'http://localhost:4000/client/main.js'
PROXYWEBSOCKET_URL = 'ws://localhost:8081/updates'
PROXYSERVER_PORT = '8080'
PROXYSERVER_URL = 'localhost:8080'
PROXYWEBSOCKET_ZMQ_LISTEN_ADDRESS = 'tcp://127.0.0.1:5555'

PROXYSERVER_CHANNEL = 'channel:proxyserver'
WEBSOCKET_CHANNEL = 'channel:websocket'
WORKER_QUEUE = 'queue:workers'

WEBSITE_URL = "http://localhost:5000"
DEBUG=True
RELOAD=True

RATE_LIMITS = [
    (10000, 60 * 60),
    (5000, 10 * 60),
    (1000, 60),
    (50, 3)
]

# Application settings
APP_NAME = "debugproxy"
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_ENABLE_CHANGE_PASSWORD = True  # Allow users to change their password
USER_ENABLE_CHANGE_USERNAME = False  # Allow users to change their username
USER_ENABLE_CONFIRM_EMAIL = True  # Force users to confirm their email
USER_ENABLE_FORGOT_PASSWORD = True  # Allow users to reset their passwords
USER_ENABLE_EMAIL = True  # Register with Email
USER_REQUIRE_RETYPE_PASSWORD = True
USER_ENABLE_USERNAME = False  # Register and Login with username
USER_AFTER_LOGIN_ENDPOINT = 'home.home_page'
USER_AFTER_LOGOUT_ENDPOINT = 'home.home_page'
USER_ENABLE_REGISTRATION = True
USER_ENABLE_INVITATION = True
USER_REQUIRE_INVITATION = True
USER_SEND_PASSWORD_CHANGED_EMAIL = False
USER_ALLOW_LOGIN_WITHOUT_CONFIRMED_EMAIL = False
USER_SHOW_EMAIL_DOES_NOT_EXIST = False
USER_SHOW_USERNAME_DOES_NOT_EXIST = False

TEMPLATES_AUTO_RELOAD = True
