import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Lobby = () => {
    const location = useLocation();
    const { socket, username, lobbyName } = location.state; // Extract socket, username, and lobby details from navigation state
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');

    useEffect(() => {
        if (socket) {
            console.log('Socket connected:', socket.connected); // Debugging log
            // Listen for chat messages from the server
            socket.on('chat_message', (data) => {
                console.log('Received chat message:', data); // Debugging log
                setMessages((prevMessages) => [...prevMessages, data]);
            });

            return () => {
                socket.off('chat_message'); // Cleanup listener on component unmount
            };
        }
    }, [socket]);

    const sendMessage = () => {
        console.log('Sending message:', newMessage); // Debugging log
        if (newMessage.trim()) {
            console.log('Sending message:', newMessage); // Debugging log
            socket.emit('chat_message', { lobby: lobbyName, username, message: newMessage });
            setNewMessage(''); // Clear input field
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