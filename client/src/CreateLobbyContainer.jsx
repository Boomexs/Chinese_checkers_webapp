import React, { useState, useEffect } from 'react';
import { useSocket } from './SocketContent.jsx';

const createLobbyContainer = ({ joinCreatedLobby }) => {
    const [lobbyName, setLobbyName] = useState('');
    const [maxPlayers, setMaxPlayers] = useState(0);
    const { socket } = useSocket();

    const handleLobbyNameChange = (event) => {
        setLobbyName(event.target.value);
    }

    const handleMaxPlayersChange = (event) => {
        setMaxPlayers(parseInt(event.target.value, 10));
    };

    const createLobby = (event) => {
        event.preventDefault();
        if (lobbyName && maxPlayers > 0) {
            console.log('Creating lobby:', lobbyName, maxPlayers);
            socket.emit('create', { lobbyname: lobbyName, needed_players: maxPlayers });
            joinCreatedLobby({ name: lobbyName, maxPlayers: maxPlayers, currentPlayers: 1 });
        }
    };

    return (
        <div>
            <h1>Create Lobby</h1>
            <form onSubmit={createLobby}>
                <label>
                    Lobby Name:
                    <input type="text" value={lobbyName} onChange={handleLobbyNameChange} />
                </label>
                <label>
                    Max Players:
                    <input type="number" value={maxPlayers} onChange={handleMaxPlayersChange}/>
                </label>
                <button type="submit">Create Lobby</button>
            </form>
        </div>
    );
}

export default createLobbyContainer;