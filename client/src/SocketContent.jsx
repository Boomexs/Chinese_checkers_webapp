// src/SocketContext.js
import React, { createContext, useContext, useState } from 'react';
import PropTypes from 'prop-types';


const SocketContext = createContext();

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);

    return (
        <SocketContext.Provider value={{ socket, setSocket }}>
            {children}
        </SocketContext.Provider>
    );
};

SocketProvider.propTypes = {
    children: PropTypes.node.isRequired,
};

export const useSocket = () => useContext(SocketContext);
