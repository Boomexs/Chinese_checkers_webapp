import { useState, useEffect } from 'react';
import { useSocket } from './SocketContent.jsx';
import { useLocation } from 'react-router-dom';
import './assets/Board.css';

const Board = () => {
    const { socket, username } = useSocket();
    const location = useLocation();
    const { lobby } = location.state || {};

    const [board, setBoard] = useState([]);
    const [currentTurn, setCurrentTurn] = useState(null);
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        socket.on('update_board', (data) => setBoard(data.board));
        socket.on('update_state', (data) => setCurrentTurn(data.state));
        socket.on('error', (data) => {
            setErrorMessage(data.message);
            setTimeout(() => setErrorMessage(null), 3000);
        });

        // Fetch initial board
        socket.emit('get_board', { lobby: lobby.name });

        return () => {
            socket.off('update_board');
            socket.off('update_state');
            socket.off('error');
        };
    }, [socket, lobby.name]);

    const onPClick = (index, id) => {
        if (currentTurn !== `turn${username}`) {
            setErrorMessage('It is not your turn!');
            return;
        }

        if (id > 0) {
            socket.emit('p_click', { lobby: lobby.name, username, index });
        } else if (id === -2) {
            socket.emit('p_move', { lobby: lobby.name, username, destination: index });
        }
    };

    const rows = (
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="board-row">
                    {row.map((item, itemIndex) => {
                        const globalCount = board
                            .slice(0, rowIndex)
                            .reduce((sum, prevRow) => sum + prevRow.length, 0) + itemIndex;

                        return (
                            <div
                                key={itemIndex}
                                onClick={() => onPClick(globalCount, item)}
                                className={`board-item p${item}-color`}
                            ></div>
                        );
                    })}
                </div>
            ))}
        </div>
    );

    return (
        <div className="board-container">
            {errorMessage && <div className="error-message">{errorMessage}</div>}
            <div className="turn-indicator">
                {currentTurn === `turn${username}` ? "It's your turn!" : "Waiting for other player..."}
            </div>
            {rows}
        </div>
    );
};

export default Board;
