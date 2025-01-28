from urllib import request

from flask_socketio import join_room, leave_room, emit, send
from move_helper import possible_moves, check_for_win
from lobby import Lobby
from moveValidator import GameStrategy1, GameStrategy2

game_variants = {
    '1': GameStrategy1(),
    '2': GameStrategy2()
}

def handle_test_connect(socketio):
    send('Connected')
    options_menu = {
        'options': ['Option 1', 'Option 2', 'Option 3']
    }
    socketio.emit('show_options', options_menu)

def handle_join(data, socketio, available_lobbies):
    username = data['username']
    lobby_name = data['lobby']
    if lobby_name in available_lobbies:
        lobby = available_lobbies[lobby_name]
        if not lobby.is_full():
            join_room(lobby_name)
            lobby.add_player(username)
            if lobby.is_full():
                lobby.game_controller.start_game()
                #lobby.state = 'turn' + str(lobby.players[0])
                socketio.emit('update_state', {
                    'state': f'turn{lobby.players[lobby.game_controller.current_player]}'
                }, room=lobby_name)
            send(f'{username} has entered the lobby', room=lobby_name)
        else:
            socketio.emit('error', {'message': 'Lobby is full.'}, room=request.sid)
    else:
        socketio.emit('error', {'message': 'Lobby not available.'}, room=request.sid)

def handle_leave(data, socketio, available_lobbies):
    username = data['username']
    lobby_name = data['lobby']
    if lobby_name in available_lobbies:
        lobby = available_lobbies[lobby_name]
        leave_room(lobby_name)
        lobby.remove_player(username)
        send(f'{username} has left the lobby', room=lobby_name)

def handle_lobby_creation(data, socketio, available_lobbies):
    lobby_name = data['lobbyname']
    max_users = data['needed_players']
    game_variant = data['game_variant']
    available_lobbies[lobby_name] = Lobby(lobby_name, max_users, game_variants[game_variant])
    socketio.emit('lobby_created', {'lobbyname': lobby_name, 'needed_players': max_users})

def handle_show_lobbies(socketio, available_lobbies):
    lobbies = [{'name': lobby_name, 'max_players': lobby.player_count, 'current_players': len(lobby.players)}
               for lobby_name, lobby in available_lobbies.items()]
    socketio.emit('lobbies_list', lobbies)

def handle_move(data, socketio, available_lobbies):
    lobby_name = data['lobby']
    player = data['player']
    move = data['move']
    if lobby_name not in available_lobbies:
        socketio.emit('error', {'message': 'Wrong lobby'}, room=request.sid)
        return
    lobby = available_lobbies[lobby_name]
    message = lobby.make_move(player, move)
    socketio.emit(message['success'], message['state'])

def handle_chat_message(data, socketio, available_lobbies):
    lobby_name = data['lobby']
    username = data['username']
    message = data['message']
    if lobby_name in available_lobbies:
        socketio.emit('chat_message', {'username': username, 'message': message}, room=lobby_name)
    else:
        socketio.emit('error', {'message': 'Lobby not available.'}, room=request.sid)

def handle_get_board(data, socketio, available_lobbies):
    lobby_name = data['lobby']
    if lobby_name in available_lobbies:
        socketio.emit('update_board', {'board': available_lobbies[lobby_name].board.board_to_data()}, room=lobby_name)

def handle_possible_moves(data, socketio, available_lobbies):
    lobby_name = data['lobby']
    index = data['index']
    lobby = available_lobbies[lobby_name]
    if lobby_name in available_lobbies:
        player = lobby.players.index(data['username']) + 1
        if player == lobby.game_controller.get_current_player():
            board_data = lobby.move_validator.possible_moves(lobby.board, index, player)
            if board_data:
                socketio.emit('update_board', {'board': board_data}, room=lobby_name)

def handle_p_move(data, socketio, available_lobbies):
    lobby_name = data['lobby']
    username = data['username']
    lobby = available_lobbies[lobby_name]

    # Get player index (1-based)
    player_index = lobby.players.index(username) + 1

    # Enforce turn
    if lobby.game_controller.get_current_player() == player_index:
        print('Handling player move...')
        destination = data['destination']
        board = lobby.board

        # Move logic
        board.flatarr[destination].content = board.selected.content
        board.selected.content = 0

        board.moves.append([destination,board.selected.id])
        print('Board moves: ', board.moves)
        # Broadcast board update
        socketio.emit('update_board', {'board': board.board_to_data()}, room=lobby_name)

        # Check for win
        if check_for_win(board, player_index):
            lobby.set_winner(username)
            socketio.emit('update_state', {'state': f'won{username}'}, room=lobby_name)
            socketio.emit('chat_message', {
                'username': 'server',
                'message': f'{username} has won the game!'
            }, room=lobby_name)
        else:
            # Proceed to the next turn
            lobby.next_turn()
            socketio.emit('update_state', {
                'state': f'turn{lobby.players[lobby.game_controller.current_player]}'
            }, room=lobby_name)
    else:
        # Not the player's turn
        socketio.emit('error', {'message': 'It is not your turn!'}, room=lobby_name)
