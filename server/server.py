from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from lobby import Lobby

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="http://localhost:5173")

available_lobbies = {
    'lobby1': Lobby('lobby1', 6),
    'lobby2': Lobby('lobby2', 2),
    'lobby3': Lobby('lobby3', 4)
}

@socketio.on('connect')
def test_connect():
    send('Connected')
    options_menu = {
        'options': ['Option 1', 'Option 2', 'Option 3']
    }
    emit('show_options', options_menu)

@socketio.on('join')
def on_join(data):
    #print(f"Join request received: {data}")  # Debugging
    username = data['username']
    lobby_name = data['lobby']
    if lobby_name in available_lobbies:
        lobby = available_lobbies[lobby_name]
        if not lobby.is_full():
            join_room(lobby_name)
            lobby.add_player(username)
            #print(f"User {username} added to {lobby_name}")  # Debugging
            send(username + ' has entered the lobby', room=lobby_name)
        else:
            send('Lobby is full.', room=request.sid)
    else:
        send('Lobby not available.', room=request.sid)

@socketio.on('leave')
def on_leave(data):
    #print(f"Leave request received: {data}")  # Debug
    username = data['username']
    lobby_name = data['lobby']
    if lobby_name in available_lobbies:
        lobby = available_lobbies[lobby_name]
        leave_room(lobby_name)
        lobby.remove_player(username)
        #print(f"{username} removed from {lobby_name}")  # Debug
        send(username + ' has left the lobby', room=lobby_name)
    #else:
        #print(f"Lobby {lobby_name} not found")  # Debug

@socketio.on('create')
def handle_lobby_creation(data):
    lobby_name = data['lobbyname']
    max_users = data['needed_players']
    available_lobbies[lobby_name] = Lobby(lobby_name, max_users)
    emit('lobby_created', {'lobbyname': lobby_name, 'needed_players': max_users})

@socketio.on('show_lobbies')
def on_show_lobbies():
    lobbies = [{'name': lobby_name, 'max_players': lobby.player_count, 'current_players': len(lobby.players)}
               for lobby_name, lobby in available_lobbies.items()]
    emit('lobbies_list', lobbies)

@socketio.on('move')
def handle_move(data):
    lobby_name = data['lobby']
    player = data['player']
    move = data['move']

    if not lobby_name in available_lobbies:
        emit('error', {'message': 'Wrong lobby'}, room=request.sid)
        return
    lobby = available_lobbies[lobby_name]
    message = lobby.make_move(player, move)
    emit(message['success'], message['state'])



@socketio.on('chat_message')
def handle_chat_message(data):
    lobby_name = data['lobby']
    username = data['username']
    message = data['message']

    if lobby_name in available_lobbies:
        emit('chat_message', {'username': username, 'message': message}, room=lobby_name)
    else:
        emit('error', {'message': 'Lobby not available'}, room=request.sid)


if __name__ == '__main__':
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)