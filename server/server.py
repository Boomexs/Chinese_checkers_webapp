from flask import Flask
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from lobby import Lobby
from handlers import *
from moveValidator import GameStrategy1, GameStrategy2



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

# Global lobby storage
available_lobbies = {
    'lobby1': Lobby('lobby1', 6, GameStrategy1()),
    'lobby2': Lobby('lobby2', 2, GameStrategy2()),
    'lobby3': Lobby('lobby3', 3, GameStrategy1())
}

@socketio.on('connect')
def on_connect():
    handle_test_connect(socketio)

@socketio.on('join')
def on_join(data):
    handle_join(data, socketio, available_lobbies)

@socketio.on('leave')
def on_leave(data):
    handle_leave(data, socketio, available_lobbies)

@socketio.on('create')
def on_create(data):
    handle_lobby_creation(data, socketio, available_lobbies)

@socketio.on('show_lobbies')
def on_show_lobbies():
    handle_show_lobbies(socketio, available_lobbies)

@socketio.on('move')
def on_move(data):
    handle_move(data, socketio, available_lobbies)

@socketio.on('chat_message')
def on_chat_message(data):
    handle_chat_message(data, socketio, available_lobbies)

@socketio.on('get_board')
def on_get_board(data):
    handle_get_board(data, socketio, available_lobbies)

@socketio.on('p_click')
def on_p_click(data):
    handle_possible_moves(data, socketio, available_lobbies)

@socketio.on('p_move')
def on_p_move(data):
    handle_p_move(data, socketio, available_lobbies)

if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)
