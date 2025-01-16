import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useSocket } from './SocketContent.jsx';
import CreateLobbyContainer from './CreateLobbyContainer';
import './assets/LobbyList.css';

const LobbyList = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { socket, setLobbyName, username } = useSocket(); // Access the socket instance from context
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
        //setLobbyName(lobby.name);
        // Ensure only serializable values are passed
        const serializableLobby = {
            name: lobby.name,
            maxPlayers: lobby.max_players,
            currentPlayers: lobby.current_players,
        };
        console.log('Joining lobby:', lobby.name);
        console.log('currentPlayers:', lobby.current_players);
        console.log('maxPlayers:', lobby.max_players);
        socket.emit('join', { username: username, lobby: lobby.name });
        navigate('/lobby', { state: { lobby: serializableLobby } });
    };


    return (
        <div className="lobby-list-container">
            <div className="lobby-list">
                <h1>Available Lobbies</h1>
                <ul>
                    {lobbies.map((lobby, index) => (
                        <li key={index}>
                            <h3>{lobby.name}</h3>
                            <p>
                                Players: {lobby.current_players}/{lobby.max_players}
                            </p>
                            <button onClick={() => joinLobby(lobby)}>Join Lobby</button>
                        </li>
                    ))}
                </ul>
            </div>
            <div className="create-lobby">
                <CreateLobbyContainer joinCreatedLobby={joinLobby}/> {/* Add the CreateLobbyContainer component */}
            </div>
        </div>
    );
};

export default LobbyList;