import React, { useState, useEffect } from 'react';
import { useSocket } from './SocketContent.jsx';

const Lobby = () => {
    const { socket, username, lobbyName } = useSocket();
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        //if (socket && socket.connected) {
            console.log('Socket connected:', socket.id);

            socket.on('chat_message', (data) => {
                console.log('Received chat message:', data);
                setMessages((prevMessages) => [...prevMessages, data]);
            });

            return () => {
                socket.off('chat_message');
            };
        //}
    }, [socket]);

    const sendMessage = () => {
        if (newMessage.trim()) {
            console.log('Socket send:', socket.id);
            console.log('Sending message:', newMessage, socket);
            const data = { lobby: lobbyName, username: username, message: newMessage };
            console.log('data:', data.lobby, data.username, data.message);
            socket.emit('chat_message', data);
            setNewMessage('');
        }
    };

    return (
        <div>
            <h1>Lobby: {lobbyName}</h1>
            <h2>Chat</h2>
            <div style={{ border: '1px solid black', height: '300px', overflowY: 'scroll', marginBottom: '10px' }}>
                {messages.map((msg, index) => (
                    <p key={index}>
                        <strong>{msg.username}: </strong>
                        {msg.message}
                    </p>
                ))}
            </div>
            <input
                type="text"
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                placeholder="Type your message"
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default Lobby;