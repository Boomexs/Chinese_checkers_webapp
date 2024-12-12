import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useSocket } from './SocketContent.jsx';

const LobbyList = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { socket } = useSocket(); // Access the socket instance from context
    const { username } = location.state || {}; // Retrieve username from state
    const [lobbies, setLobbies] = useState([]);

    useEffect(() => {
        if (!socket) {
            // If socket is undefined, redirect to the login page
            navigate('/');
            return;
        }

        // Request the lobbies list
        socket.emit('show_lobbies');

        // Listen for the lobbies list
        socket.on('lobbies_list', (data) => {
            console.log('Lobbies received:', data);
            setLobbies(data);
        });

        // Clean up socket listeners
        return () => {
            socket.off('lobbies_list');
        };
    }, [socket, navigate]);

    const joinLobby = (lobby) => {
        // Ensure only serializable values are passed
        const serializableLobby = {
            name: lobby.name,
            maxPlayers: lobby.maxPlayers,
            currentPlayers: lobby.currentPlayers,
        };
        navigate('/lobby', { state: { lobby: serializableLobby } });
    };

    return (
        <div>
            <h1>Available Lobbies</h1>
            <ul>
                {lobbies.map((lobby, index) => (
                    <li key={index}>
                        <h3>{lobby.name}</h3>
                        <p>
                            Players: {lobby.current_players}/{lobby.max_players}
                        </p>
                        <button onClick={() => joinLobby(lobby.name)}>Join Lobby</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default LobbyList;
