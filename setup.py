from setuptools import setup, find_packages
from codecs import open
from os import path

setup(
    name='debugproxy',
    version='0.0.1',
    description='debug proxy server',
    long_description='no long description',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        # Proxy Server
        'mitmproxy',
        'aioredis',
        'rratelimit',

        # Proxy Web
        'gunicorn',
        'psycopg2',
        'Flask',
        'Flask-Login',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-User',
        'requests',

        # Development
        'pytest',
        'pytest-flask',
        'pytest-cov',
        'pytest-capturelog',
        'testfixtures',
        'Flask-Assets',
        'webassets',
        'cssmin'
    ],

    entry_points={
        'console_scripts': [
            'proxyserver=proxyserver:proxyserver',
            'proxywebsocket=proxyserver:proxywebsocket',
            'proxyworker=proxyserver:proxyworker',
            'status=monitoring:print_stats',
            'munin=monitoring:munin_stats',
            'generate-certificates=proxyserver:generate_certificates'
        ],
    }
)
