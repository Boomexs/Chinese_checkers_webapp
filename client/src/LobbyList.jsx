import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const LobbyList = () => {
    const location = useLocation();
    const { socket, username } = location.state; // Retrieve socket and username
    const [lobbies, setLobbies] = useState([]);

    useEffect(() => {
        if (socket) {
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
        }
    }, [socket]);

    const joinLobby = (lobbyName) => {
        socket.emit('join', { username, lobby: lobbyName });
        console.log(`Joining lobby: ${lobbyName}`);
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
