from db import db
from typing import List
from sqlalchemy.sql import func
from flask_sqlalchemy import Pagination
import jwt
import datetime
from config import SECRET_KEY

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=func.now())
    updated_at = db.Column(db.DateTime, onupdate=func.now())

    def __init__(self, username, password,email,created_at = func.now(),updated_at = func.now()):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return 'UserModel(username=%s, email=%s, password=%s,author_id=%s,created_at=%s,updated_at=%s)' % (self.username, self.email, self.password,self.created_at,self.updated_at)

    def json(self):
        return {'username': self.username, 'email': self.email, 'password': self.password, 'created_at': self.created_at, 'updated_at': self.updated_at}

    @classmethod
    def find_by_username_and_password(cls, _username,_password) -> "UserModel":
        return cls.query.filter_by(username =_username,password=_password).first()
    
    @classmethod
    def find_by_email_and_password(cls, _email,_password) -> "UserModel":
        return cls.query.filter_by(email =_email,password=_password).first()
    
    @classmethod
    def find_by_username(cls, _username,) -> "UserModel":
        return cls.query.filter_by(username =_username).first()
    
    @classmethod
    def find_by_email(cls, _email,) -> "UserModel":
        return cls.query.filter_by(email =_email).first()

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()    

    def encode_auth_token(self,user_id):
     try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0,minutes=60, seconds=3),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
           SECRET_KEY,
            algorithm='HS256'
        )
     except Exception as e:
        return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, SECRET_KEY,algorithms=["HS256"])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False