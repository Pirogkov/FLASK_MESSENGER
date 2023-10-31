from flask import render_template, redirect, url_for, current_app, flash, jsonify, json, request, make_response, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_socketio import join_room, leave_room, send, SocketIO, emit, rooms
from datetime import datetime
import functools

from app.models import User, Message, ActiveRoom
from app import socketio, db
from app.chat import bp
from app.define.query import return_messages


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped




# @bp.before_request
# def before_request():
#     if current_user.is_authenticated and current_user.is_user():
#         if not ActiveRoom.is_exists():
#             new_room = ActiveRoom(room=current_user.room, active_users=1)
#             db.session.add(new_room)
#             db.session.commit()


@bp.route('/messenger', methods=['GET', 'POST'])
@login_required
def messenger():
    if current_user:
        room = current_user.room
        if request.method == 'GET':
            return render_template('chat/messenger.html', code=room)
        if request.method == 'POST':
            # if not session.modified:
            #     session.modified = True
            data = Message.get_messages(room)
            response = make_response(data)
            response.headers['User-InfoName'] = current_user.username
            return response


@bp.route('/operator_room', methods=['GET', 'POST'])
@login_required
def operator_room():
    if current_user.is_admin():
        users_rooms = ActiveRoom.query.all()
        return render_template('chat/operator_room.html', users_rooms=users_rooms)
    return render_template('index.html', flash='Вход запрещён!')




@bp.route('/operator_messenger/<room_name>', methods=['GET', 'POST'])
@login_required
def operator_joinroom(room_name):
    if current_user.is_admin():
        current_user.room = room_name
        room = ActiveRoom.query.filter_by(room=current_user.room).first()
        room.active_users = 2
        db.session.commit()
        return render_template('chat/messenger.html', code=f'Оператор в комнате {current_user.room}')
    return render_template('index.html', flash='Вход запрещён!')


#
#
#
#

@socketio.on("connect")
@authenticated_only
def connect():
    test = request.sid
    print(current_user, 'Подключился', test)
    room = current_user.room
    name = current_user.username
    time = datetime.utcnow().isoformat()
    join_room(room)
    if current_user.is_user():
        print(current_user.is_user())
        if not ActiveRoom.is_exists():
            print(ActiveRoom.is_exists())
            new_room = ActiveRoom(room=current_user.room, active_users=1, new_messages=0)
            db.session.add(new_room)
            db.session.commit()
    if current_user.is_admin():
        emit('connect', {'name': name, 'message': 'подключился к чату', 'timestamp': time}, to=room)



@socketio.on("disconnect")
@authenticated_only
def disconnect():
    print(current_user, 'Отключился')
    room = current_user.room
    name = current_user.username
    time = datetime.utcnow().isoformat()
    leave_room(room)
    active_room = ActiveRoom.query.filter_by(room=room).first()
    if current_user.is_admin():
        active_room.active_users = 1
        emit('disconnect', {'name': name, 'message': 'покинул чату', 'timestamp': time}, to=room)
    if current_user.is_user() and active_room.new_messages == 0:
        ActiveRoom.query.filter_by(room=room).delete()
    db.session.commit()


#
#
@socketio.on("message")
@authenticated_only
def message(data):
    room = current_user.room
    time = datetime.utcnow().isoformat()
    content = {
        "name": current_user.username,
        "message": data["data"],
        "timestamp": time
    }
    print(content)
    send(content, to=room)
    message = Message(name=current_user.username, message=data["data"], room=room)
    get_room = ActiveRoom.query.filter_by(room=room).first()
    if current_user.is_user():
        if get_room.active_users == 1:
            get_room.new_messages += 1
        db.session.add(get_room)
    if current_user.is_admin():
        get_room.active_users = 2
        get_room.new_messages = 0
    db.session.add(message)
    db.session.commit()
