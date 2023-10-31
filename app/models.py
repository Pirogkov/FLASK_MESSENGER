import json

from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify

from datetime import datetime
import random
from string import ascii_uppercase
import enum

from app import db, login


class User(UserMixin,  db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    user_role = db.Column(db.String(64), default='User')
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    ls = db.Column(db.String(12), index=True, unique=True)
    room = db.Column(db.String(16))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_message_read_time = db.Column(db.DateTime, index=True)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def chek_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def generate_room_code(self, length: int = 12) -> None:
        code: str = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        self.room = code

    def is_admin(self):
        if self.user_role == 'Admin':
            return True
        return False

    def is_user(self):
        if self.user_role == 'User':
            return True
        return False


class Message(db.Model):
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(16))
    name = db.Column(db.String(64), index=True)
    message = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __repr__(self):
        return "<name={}, " \
               "message={}, " \
               "room={}, " \
               "timestamp={}".format(self.name, self.message, self.room, self.timestamp)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'message': self.message,
            'room': self.room,
            'timestamp': self.timestamp.isoformat()
        }

    @staticmethod
    def get_messages(room) -> list:
        get_messeges = db.session.query(Message).filter_by(room=room)
        data = [x.serialize for x in get_messeges.all()]
        return data


class ActiveRoom(db.Model):
    __tablename__ = "activeroom"

    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    active_users = db.Column(db.Integer())
    new_messages = db.Column(db.Integer)

    @staticmethod
    def is_exists():
        is_exists = ActiveRoom.query.filter_by(room=current_user.room).count()
        if is_exists == 0:
            return False
        return True


