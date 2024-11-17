import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState, useContext} from 'react';
import { SocketContext } from '../../SocketProvider';
import { toast } from 'react-hot-toast';
import './GamePlay.css';
import circle_pic from '../Images/circle.png';
import x_pic from '../Images/x.png';
import cookie from '../utils/cookie';

const GamePlay = ({ currentUser, setCurrentUser }) => {
    const { gameId } = useParams();
    let [count, setCount] = useState(0);
    let [lock, setLock] = useState(false);
    let [board, setBoard] = useState(Array(9).fill(""));

    const navigate = useNavigate();
    const socket = useContext(SocketContext);
    console.log(currentUser);

    const playAgain = async (game_state) => {
        const won = game_state['won'];
        const player = game_state['player'];

        const response = await new Promise((resolve) => {
            var text = "";
        if (won === "True"){
            text = `'${player}' won the game!!`;
        }
        else {
            text = "There was a draw!";
        }
            toast((t) => (
              <span>
                {text}<br />
                Want to play again?<br />
                <button onClick={() => {
                  resolve(handleAccept());
                  toast.dismiss(t.id);
                }}
                style={{ margin: '8px 8px', padding: '4px 8px' }}>
                  Play Again?
                </button>
                <button
                onClick={() => {
                  toast.dismiss(t.id);
                  resolve(handleDecline());
                }}
                style={{ margin: '8px 8px', padding: '4px 8px' }}>
                Quit
              </button>
              </span>
            ), {position: "top-center", duration: Infinity});
    
            const handleAccept = () => {
              return "accepted";
            };
          
            const handleDecline = () => {
              return "quit";
            };
        });
            return (
              response
            );
    };

    useEffect(() => {
        // Use the gameId for game-specific actions, like joining a socket room
        socket.emit('join_game', { 'gameId': gameId, 'user': currentUser.userID });

        socket.on('load_board', (data) => {
            const board = data['board'];
            const currentUser = data['user'];
            setBoard(board);
            console.log(`current user: ${currentUser}`);
        });

        socket.on('move_made', async(data) =>{
            const index = data['index'];
            const player = data['player'];
            const won = data['game_state'];
            // const next_player = data['next_player'];
            
            if (currentUser['symbol'] ==  next_player) {
                setLock(false);
                // setCurrentUser(next_player);
            }

            setBoard((prevBoard) => {
                const newBoard = [...prevBoard];
                newBoard[index] = player;
                return newBoard;
            });

            console.log(board)
            if (count == 0)
                setCount((prevCount) => prevCount + 1);
            if (won === 'True' || won === 'Draw') {
                setLock(true)
                const response = await playAgain({'won': won, 'player': player});
                if (response === "accepted") {
                    setBoard(Array(9).fill(""));
                    setLock(false);
                    setCount(0);
                    socket.emit('new_game', {'game_id' : gameId});
                }
                else{
                    navigate('/lobby');
                }
            }
        });

        return () => {
            // Clean up: Optionally leave the room if needed when component unmounts
            socket.emit('leave_game', { gameId });
            socket.off('load_board');
            socket.off('move_made');
        };
    }, [gameId]);

    const toggle = (index) => {
        if (lock || board[index]) {
            return;
        }
        console.log('Board button pressed');
        let player;
        player = count % 2 == 0 ? "X" : "O";
        var next_player = player === "X" ? "O" : "X";
        //if (currentUser['symbol'] !== next_player) {
            setBoard(prevBoard => {
                const newBoard = [...prevBoard];
                newBoard[index] = player;
                return newBoard;
            });
            socket.emit('make_move', {'game_id': gameId, 'index': index, 'player': currentUser.userID})
            // socket.emit('make_move', { 'game_id': gameId, 'index': index, 'player': player, 'next_player': next_player});
        //}
        //setLock(true);
    }

    return(
        <div className="CONTAINER">
            <h1 className="title">Play Game!</h1>
            <div className="board">
                {board.map((cell, index) => (
                    <div
                        key={index}
                        className="boxes"
                        onClick={() => toggle(index)}
                    >
                        {cell && (
                            <img
                                src={cell === "X" ? x_pic : circle_pic}
                                alt={cell}
                            />
                        )}
                    </div>
                ))}
            </div>
        </div>
    )
};

export default GamePlay;
