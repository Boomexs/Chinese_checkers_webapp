import unittest
from pyexpat.errors import messages

from flask import Flask
from flask_socketio import SocketIO, emit
from flask_socketio import SocketIOTestClient

# Import the app and socketio from your server file
from server import app, socketio

class TestSocketIO(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.socketio = socketio
        self.client = self.socketio.test_client(self.app)
        self.client2 = self.socketio.test_client(self.app)

    def test_options_menu_on_connect(self):
        self.client.connect()

        received = self.client.get_received()
        self.assertTrue(any(event['name'] == 'show_options' for event in received))

        for event in received:
            if event['name'] == 'show_options':
                self.assertEqual(event['args'][0]['options'], ['Option 1', 'Option 2', 'Option 3'])

    def test_create_lobby(self):
        self.client.connect()
        self.client.emit('create', {'lobbyname': 'new_lobby', 'needed_players': 6})
        received = self.client.get_received()
        created_event = [event for event in received if event['name'] == 'lobby_created']
        self.assertTrue(len(created_event) > 0)
        self.assertEqual(created_event[0]['args'][0]['lobbyname'], 'new_lobby')


    def test_join_lobby(self):
        self.client.connect()
        self.client.emit('join', {'username': 'test_user', 'lobby': 'lobby1'})
        received = self.client.get_received()
        print("Received events:", received)  # Debugging

        self.assertTrue(
            any(event['name'] == 'message' and event['args'] == 'test_user has entered the lobby' for event in received),
            "Expected join confirmation message not received."
        )


    def test_leave_lobby(self):
        self.client.connect()
        self.client2.connect()
        self.client2.emit('join', {'username': 'listener', 'lobby': 'lobby1'})
        self.client.emit('join', {'username': 'test_user', 'lobby': 'lobby1'})
        self.client.emit('leave', {'username': 'test_user', 'lobby': 'lobby1'})
        received = self.client2.get_received()

        #print("Received events during leave:", received)  # Debugging
        messages = [msg['args'] for msg in received if msg['name'] == 'message']
        #print("Extracted messages:", messages)  # Debugging

        self.assertIn('test_user has left the lobby', messages)

    def test_group_chat(self):
        self.client.connect()
        self.client2.connect()
        self.client2.emit('join', {'username': 'user2', 'lobby': 'lobby1'})
        self.client.emit('join', {'username': 'user1', 'lobby': 'lobby1'})

        self.client.emit('chat_message', {'username': 'user1', 'lobby': 'lobby1', 'message': 'hi user2'})
        self.client2.emit('chat_message', {'username': 'user2', 'lobby': 'lobby1', 'message': 'hi user1'})

        received1 = self.client.get_received()
        message1 = [msg['args'][0] for msg in received1 if msg['name'] == 'chat_message']

        received2 = self.client2.get_received()
        message2 = [msg['args'][0] for msg in received2 if msg['name'] == 'chat_message']

        self.assertEqual(message1, [{'username': 'user1', 'message': 'hi user2'}, {'username': 'user2', 'message': 'hi user1'}])
        self.assertEqual(message2, [{'username': 'user1', 'message': 'hi user2'}, {'username': 'user2', 'message': 'hi user1'}])





    def tearDown(self):
        self.client.disconnect()

if __name__ == '__main__':
    unittest.main()