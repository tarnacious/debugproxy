from flask.sessions import TaggedJSONSerializer
from config.default_settings import SECRET_KEY
import datetime
import hashlib
from itsdangerous import URLSafeTimedSerializer
from typing import Any


def read_session(string: str) -> Any:
    serializer = TaggedJSONSerializer()
    signer_kwargs = dict(
        key_derivation='hmac',
        digest_method=hashlib.sha1
    )
    safeTimeSerializer = URLSafeTimedSerializer(SECRET_KEY,
                                                salt='cookie-session',
                                                serializer=serializer,
                                                signer_kwargs=signer_kwargs)

    max_age = 2678400 # 31 days
    data = safeTimeSerializer.loads(string, max_age=max_age)
    return data


from flask_user.token_manager import TokenManager

class FakeFlaskApp(object):
    @property
    def config(self):
        return {
            'SECRET_KEY': SECRET_KEY
        }

def decrypt_user_id(cipher_text):
    token_manager = TokenManager(FakeFlaskApp())
    return token_manager.verify_token(cipher_text)[0]

from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['bcrypt'])

def verify_password(password: str, hashed_password: str) -> bool:

    # Generate SHA512 HMAC -- For compatibility with Flask-Security
    # We're not *currently* using this, but maybe we should.
    # password = generate_sha512_hmac(user_manager.password_salt, password)

    return crypt_context.verify(password, hashed_password)
