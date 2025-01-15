import React from 'react';
import './assets/Board.css';

const BoardItem = (index) => {
    return <div key={index} className="board-item">
        Item {index}
    </div>
};

const Board = () => {
    const itemCounts = [1, 2, 3, 4, 5, 13, 12, 11, 10, 11, 12, 13, 5, 4, 3, 2, 1];
    let itemIndex = 0;

    const rows = itemCounts.map((count, rowIndex) => (
        <div key={rowIndex} className="board-row">
            {Array.from({ length: count }, () => (
                <div key={itemIndex} className="board-item">
                    Item {itemIndex++}
                </div>
            ))}
        </div>
    ));

    return <div className="board-container">{rows}</div>;
};

export default Board;