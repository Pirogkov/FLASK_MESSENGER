from app import create_app, db, socketio


app = create_app()

6
if __name__ == '__main__':
    socketio.run(app, host='10.4.136.63', port=5000, debug=True)