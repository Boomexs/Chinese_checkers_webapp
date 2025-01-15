import { useState, useEffect } from 'react';
import { useSocket } from './SocketContent.jsx';
import { useNavigate, useLocation } from 'react-router-dom';
import Board from './Board.jsx';
import './assets/Lobby.css';

const Lobby = () => {
    const { socket, username } = useSocket();
    const [messages, setMessages] = useState([]);
    const [newMessage, setNewMessage] = useState('');
    const [currentPlayers, setCurrentPlayers] = useState(0);
    const [maxPlayers, setMaxPlayers] = useState(0);
    const navigate = useNavigate();
    const location = useLocation();
    const { lobby } = location.state || {}; // Access lobby from navigation state

    useEffect(() => {
        if (!lobby) {
            console.warn('Lobby not provided, redirecting...');
            navigate('/');
            return;
        }

        console.log('Lobby data:', lobby); // Debug lobby data
        setCurrentPlayers(lobby.currentPlayers || 0); // Default to 0 if undefined
        setMaxPlayers(lobby.maxPlayers || 0); // Default to 0 if undefined

        console.log('Socket connected:', socket.id); // Debug socket connection

        socket.on('chat_message', (data) => {
            console.log('Received chat message:', data);
            setMessages((prevMessages) => [...prevMessages, data]);
        });

        socket.on('player_joined', (data) => {
            console.log('Player joined:', data);
            setCurrentPlayers(data.currentPlayers || 0);
        });

        socket.on('player_left', (data) => {
            console.log('Player left:', data);
            setCurrentPlayers(data.currentPlayers || 0);
        });

        return () => {
            socket.off('chat_message');
            socket.off('player_joined');
            socket.off('player_left');
        };
    }, [socket, lobby, navigate]);

    const sendMessage = () => {
        if (newMessage.trim()) {
            console.log('Sending message:', newMessage);
            socket.emit('chat_message', {
                lobby: lobby.name,
                username,
                message: newMessage,
            });
            setNewMessage('');
        }
    };

    const leaveLobby = () => {
        socket.emit('leave', { username: username, lobby: lobby.name });
        navigate('/lobbies');
    };

    return (
        <div className="lobby-content">
            <div className="lobby-container">
                <div className="lobby-header">
                    <h1>Lobby: {lobby?.name || 'Unknown'}</h1>
                    <h2>Players: {currentPlayers}/{maxPlayers}</h2>
                </div>
                <div className="chat-container">
                    {messages.map((msg, index) => (
                        <p key={index} className="chat-message">
                            <strong>{msg.username}: </strong>
                            {msg.message}
                        </p>
                    ))}
                </div>
                <div className="input-container">
                    <input
                        type="text"
                        value={newMessage}
                        onChange={(e) => setNewMessage(e.target.value)}
                        placeholder="Type your message"
                    />
                    <button onClick={sendMessage}>Send</button>
                    <button onClick={leaveLobby}>Leave Lobby</button>
                </div>
            </div>
            <div className="board-container">
                <Board />
            </div>
        </div>
    );
};

export default Lobby;