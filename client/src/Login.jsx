import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import { io } from 'socket.io-client';

const Login = () => {
    const [username, setUsername] = useState('');
    const [socketPort, setSocketPort] = useState('');
    const navigate = useNavigate();

    const handleUsername = (event) => {
        setUsername(event.target.value);
    };

    const handleSocketPort = (event) => {
        setSocketPort(event.target.value);
    };

    const connect = () => {
        // Establish socket connection to the specified port
        const socketConnection = io(`http://localhost:${socketPort}`);

        socketConnection.on('connect', () => {
            console.log('Connected to server on port', socketPort);

            // Navigate to the lobbies page, passing socket and username
            navigate('/lobbies', { state: { socket: socketConnection, username } });
        });

        socketConnection.on('show_options', (data) => {
            console.log('Options:', data.options);
        });

        socketConnection.on('message', (message) => {
            console.log('Message:', message);
        });
    };

    return (
        <>
            <h1>Log in</h1>
            <div style={{ marginBottom: '20px' }}>
                <label>
                    Username: {' '}
                    <input value={username} onChange={handleUsername} />
                </label>
            </div>
            <div style={{ marginBottom: '20px' }}>
                <label>
                    Socket Port: {' '}
                    <input value={socketPort} onChange={handleSocketPort} />
                </label>
            </div>
            <button onClick={connect}>Connect</button>
        </>
    );
};

export default Login;
