from datetime import datetime

from config import read_config
from flask_user import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, \
                         BadSignature
import sqlalchemy as db
from database.database import Base
from sqlalchemy.orm import relationship, backref

config = read_config()

class Organization(Base):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),
                     nullable=False,
                     server_default=u'',
                     unique=True)
    users = relationship('User', backref=backref('users'))


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255),
                      nullable=False,
                      server_default=u'',
                      unique=True)

    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100),
                                     nullable=False,
                                     server_default='')

    # User information
    active = db.Column('is_active',
                       db.Boolean(),
                       nullable=False,
                       server_default='0')

    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')

    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())

    # Relationships
    roles = relationship('Role', secondary='users_roles',
                            backref=backref('users', lazy='dynamic'))

    organization_id = db.Column(db.Integer(),
                                db.ForeignKey('organizations.id',
                                              ondelete='CASCADE'),
                                nullable=False)

    proxy_sessions = relationship('ProxySession',
                                  cascade='all,delete',
                                  backref=backref('proxy_sessions'))

    @property
    def is_admin(self) -> bool:
        return self.has_role('admin')

    def generate_auth_token(self) -> str:
        sig = TimedJSONWebSignatureSerializer(
            config['SECRET_KEY'],
            expires_in=config['TOKEN_INVALIDATION_SECONDS']
        )
        return sig.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token: str) -> bool:
        s = TimedJSONWebSignatureSerializer(config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        return User.get_by_id(data['id'])

    @classmethod
    def get_by_id(cls, record_id: str) -> Base:
        if any(
                (isinstance(record_id, str) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))
        return None


class ProxySession(Base):
    __tablename__ = 'proxy_session'
    id = db.Column(db.Integer(), primary_key=True)

    user_id = db.Column(db.Integer(),
                        db.ForeignKey('users.id',
                                      ondelete='CASCADE'),
                        nullable=False)

    username = db.Column(db.String(255),
                         nullable=False,
                         unique=True)

    password = db.Column(db.String(255),
                         nullable=False)

    is_active = db.Column(db.Boolean(),
                          nullable=False,
                          server_default='1')

    requests = relationship('Request',
                                cascade="all,delete",
                                backref=backref('requests'))

    intercepts = relationship('Intercept',
                                cascade="all,delete",
                                backref=backref('intercepts'))

    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=db.func.now())


class Intercept(Base):
    __tablename__ = 'intercept'

    id = db.Column(db.Integer(), primary_key=True)

    session_id = db.Column(db.Integer(),
                           db.ForeignKey('proxy_session.id',
                                         ondelete='CASCADE'),
                           nullable=False)

    query = db.Column(db.String(255),
                      nullable=False)

    method = db.Column(db.String(255),
                       nullable=False)

# CREATE INDEX CONCURRENTLY request_key_index ON request (key);
# CREATE INDEX CONCURRENTLY request_session_id_index ON request (session_id);
# CREATE INDEX CONCURRENTLY request_created_at_index ON request (created_at);
# ALTER TABLE request SET (autovacuum_vacuum_scale_factor = 0.0);
# ALTER TABLE request SET (autovacuum_vacuum_threshold = 5000);
# ALTER TABLE request SET (autovacuum_analyze_scale_factor = 0.0);
# ALTER TABLE request SET (autovacuum_analyze_threshold = 5000);

class Request(Base):
    __tablename__ = 'request'

    id = db.Column(db.Integer(), primary_key=True)

    key = db.Column(db.String(255),
                    nullable=False)

    session_id = db.Column(db.Integer(),
                           db.ForeignKey('proxy_session.id',
                                         ondelete='CASCADE'),
                           nullable=False)

    state = db.Column(db.JSON())
    proxyserver = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())


class Role(Base):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


class UsersRoles(Base):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class UserInvitation(Base):
    __tablename__ = 'user_invite'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    # save the user of the invitee
    invited_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # token used for registration page to identify user registering
    token = db.Column(db.String(100), nullable=False, server_default='')
    created_at = db.Column(db.DateTime(timezone=True), default=db.func.now())
