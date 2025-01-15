import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { io } from 'socket.io-client';
import { useSocket } from './SocketContent.jsx';
import './assets/Login.css'; // Import the CSS file

const Login = () => {
    const [username, setUsername] = useState('');
    const [socketPort, setSocketPort] = useState('');
    const { setSocket, setUsername: setContextUsername } = useSocket();
    const navigate = useNavigate();

    const handleUsername = (event) => {
        setUsername(event.target.value);
    };

    const handleSocketPort = (event) => {
        setSocketPort(event.target.value);
    };

    const connect = () => {
        const socketConnection = io(`http://localhost:${socketPort}`);

        socketConnection.on('connect', () => {
            console.log('Connected to server on port', socketPort);
            setSocket(socketConnection);
            setContextUsername(username);
            navigate('/lobbies', { state: { username } });
        });

        socketConnection.on('show_options', (data) => {
            console.log('Options:', data.options);
        });

        socketConnection.on('message', (message) => {
            console.log('Message:', message);
        });
    };

    return (
        <div className="login-container">
            <h1 className="login-title">Log in</h1>
            <div className="login-field">
                <label>
                    Username: {' '}
                    <input value={username} onChange={handleUsername} />
                </label>
            </div>
            <div className="login-field">
                <label>
                    Socket Port: {' '}
                    <input value={socketPort} onChange={handleSocketPort} />
                </label>
            </div>
            <button className="login-button" onClick={connect}>Connect</button>
        </div>
    );
};

export default Login;