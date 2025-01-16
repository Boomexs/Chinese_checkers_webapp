import { useState, useEffect, useContext } from 'react';
import { useSocket } from './SocketContent.jsx';
import { useNavigate, useLocation } from 'react-router-dom';
import './assets/Board.css';

const BoardItem = (index) => {
    return <div key={index} className="board-item">
        Item {index}
    </div>
};

const Board = () => {
    // Used for preparing a dummy board
    const itemCounts = [
        1,
        2,
        3,
        4,
        13,
        12,
        11,
        10,
        9,
        10,
        11,
        12,
        13,
        4,
        3,
        2,
        1,
    ]
    const totalIDs = itemCounts.reduce((acc, num) => acc + num, 0);

    const { socket, username } = useSocket();
    const location = useLocation();
    const { lobby } = location.state || {};
    const [ board, setBoard ] = useState([[1,1],[2,2]]);
    const [turn, setTurn ] = useState('waiting')

    useEffect(() => {
      socket.on('update_state', (data) => {
          console.log('update_state:',data);
          setTurn(data['state'])
      })

  }, [socket])


    useEffect(()=>{
        socket.on('update_board',(data) => {
            setBoard(data['board']);
        });

        socket.emit('get_board', {'lobby': lobby.name});
    },[socket]);

    const onPClick = (index,id) => {
      console.log(('turn' + username))
      console.log(turn === 'turn' + username)
      if(turn === ('turn' + username) && id > 0){
        socket.emit('p_click', {'lobby': lobby.name, 'username': username, 'index': index});
      }else if(turn === ('turn' + username) && id == -2){
        socket.emit('p_move', {'lobby': lobby.name, 'username': username, 'destination': index});
      }
    };

    // socket.emit('get_board', {'lobby': lobby.name});

    let itemIndex = 0;

    // const rows = itemCounts.map((count, rowIndex) => (
    //     <div key={rowIndex} className="board-row">
    //         {Array.from({ length: count }, () => (
    //             <div key={itemIndex} className="board-item">
    //                 Item {itemIndex++}
    //             </div>
    //         ))}
    //     </div>
    // ));
//     const rows = 
//   <div className="board">
//     {board.map((row, rowIndex) => (
//       <div key={rowIndex} className="board-row">
//         {row.map((item, itemIndex) => (
//           <div key={itemIndex} onClick={() => {onPClick(itemIndex)}} className={'board-item ' + ('p' + item + '-color ')}>
//             {item}
//           </div>
//         ))}
//       </div>
//     ))}
//   </div>
const rows = 
<div className="board">
{board.map((row, rowIndex) => (
  <div key={rowIndex} className="board-row">
    {row.map((item, itemIndex) => {
      // calc global count
      const globalCount = board
        .slice(0, rowIndex) // get prev rows
        .reduce((sum, prevRow) => sum + prevRow.length, 0) + itemIndex;

      return (
        <div
          key={itemIndex}
          onClick={() => onPClick(globalCount,item)}
          className={`board-item p${item}-color`}
        >
          {/* {globalCount} Display the global count */}
        </div>
      );
    })}
  </div>
))}
</div>

    return <div className="board-container">{rows}</div>;
};

export default Board;