from ..models import User, Message, ActiveRoom
from app import db


def return_messages(room):
    get_messages = db.session.query(Message.name, Message.message).filter_by(room=room).all()
    return get_messages

