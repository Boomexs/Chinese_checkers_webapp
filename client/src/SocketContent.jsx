// src/SocketContext.js
import React, { createContext, useContext, useState } from 'react';
import PropTypes from 'prop-types';


const SocketContext = createContext();

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const [username, setUsername] = useState('');
    const [lobbyName, setLobbyName] = useState('');

    return (
        <SocketContext.Provider value={{ socket, setSocket, username, setUsername, lobbyName, setLobbyName }}>
            {children}
        </SocketContext.Provider>
    );
};

SocketProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export const useSocket = () => useContext(SocketContext);
