# debugProxy

Very early hacking on multi session debugging proxy server.

## Overview

The goal of the project is to provide hosted proxy server and a web based user
interface to view and modify traffic through the proxy.

The projects is made up of several components.

* proxyweb - server side web user interface and user management
* proxyui - client side proxy user interface
* proxyserver - proxy server and websocket server
* proxyworker - authenticate proxy requests, lookup intercepts, store requests
* proxywebsocket - websocket server for sending request details to the client

## Python environment

All server components run on Python 3.7. This readme assumes an isolated python
environment, eg with virtualenv.

    virtualenv .
    source ./bin/activate



    pip install -r requirements.txt
    python setup.py develop

## Services

A PostgreSQL is required, it can be run as docker container for testing and
development.

    docker-compose up

The default user is `postgres` and the password `password`.


## Initializing the Database

The project depends on a Postgres databases called `website` and `website-test`
in the default config.

    createdb -U postgres website
    createdb -U postgres website-test

A Python script initializes the database. This creates tables, adds an
organization and a system admin user.

    ./bin/python manage.py init_db

The database can be seeded with some example data.

    ./bin/python manage.py seed_db

This creates two users:

    username: admin@debubproxy.de
    password: password

and

    username: user@debugproxy.de
    password: password


Databases can also be dropped, if needed.

    ./bin/python manage.py drop_db


## proxyweb

### Running in development

Requires the `sass` program. Unfortunately this requires ruby.

    ./bin/python manage.py runserver

Proxyweb binds to `localhost:5000`.

### Running in production

The example environment-specific settings are found in proxyserver/default_setting.py

    export DEBUGPROXY_SETTING_FILE=/path/to/settings.py

The app should be run through gunicorn

    ./bin/gunicorn manage:app

## proxyui

The UI requires `Node.js > 5` and `npm`. It is currently built and run from the
`proxyui` directory:

    cd proxyui
    npm install
    npm run

The readme in the `proxyui` directory contains more information about running
the tests and building assets.

## proxyserver

Run the server

    ./bin/proxyserver

Proxy a request (you create username and passwords in the web ui)

    curl theage.com.au --proxy user:password@localhost:8080

Should see request appear in traffic page for this username/password session.

### ssl certificates

The SSL root certificate and client certificates are generated and saved to
`~/.mitmproxy` when the proxyserver is first run. The client certificates can
also be downloaded by visiting `localhost:5000/certificates` through the proxy.

To generate custom "debugproxy" SSL certificates, remove the generated
mitmproxy certificates and generate new ones.

    rm -rf ~/.mitmproxy
    ./bin/generate-certificates

## proxywebsocket

Run the server

    ./bin/proxywebsocket

## proxyworker

Run the server

  ./bin/proxyworker

## simpleserver

Run a proxyserver, a proxyworker and proxywebsocket

  ./bin/simpleserver

## Testing

Run unit tests

    ./bin/py.test -s tests/

Check static typing

    ./bin/mypy --ignore-missing-imports --disallow-untyped-defs  .

## Coverage

    ./bin/py.test -s --cov-report term-missing --cov-config tests/.coveragerc --cov app tests/
