from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return 'localhost'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip')
def ip():
    return jsonify({'ip': get_local_ip()})

@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    username = data.get('username', 'Unknown')
    join_room(room)
    emit('status', {'msg': f"{username} 님이 입장했습니다."}, room=room)

@socketio.on('text')
def handle_text(data):
    room = data.get('room')
    username = data.get('username', 'Unknown')
    msg = data.get('msg', '')
    emit('message', {'msg': f"{username}: {msg}"}, room=room)

@socketio.on('offer')
def handle_offer(data):
    room = data.get('room')
    emit('offer', data, room=room, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    room = data.get('room')
    emit('answer', data, room=room, include_self=False)

@socketio.on('candidate')
def handle_candidate(data):
    room = data.get('room')
    emit('candidate', data, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
