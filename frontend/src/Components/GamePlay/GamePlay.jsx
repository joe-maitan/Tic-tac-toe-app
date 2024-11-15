import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState, useContext} from 'react';
import { SocketContext } from '../../SocketProvider';
import { toast } from 'react-hot-toast';
import './GamePlay.css';
import circle_pic from '../Images/circle.png'
import x_pic from '../Images/x.png'

const GamePlay = () => {
    const { gameId } = useParams();
    let [count, setCount] = useState(0);
    let [lock, setLock] = useState(false);
    let [board, setBoard] = useState(Array(9).fill(""));

    const socket = useContext(SocketContext);

    useEffect(() => {
        // Use the gameId for game-specific actions, like joining a socket room
        socket.emit('join_game', { 'gameId': gameId });
        console.log("in room with game_id: " + gameId);

        socket.on('load_board', (data) => {
            const board = data['board'];
            setBoard(board);
        });

        socket.on('move_made', (data) => {
            console.log("in move_made");
            toast.success("Move was made!");
            const index = data['index'];
            const player = data['player'];
            const won = data['won'];
            setBoard((prevBoard) => {
                const newBoard = [...prevBoard];
                newBoard[index] = player;
                return newBoard;
            });
            console.log(board)
            if (count == 0)
                setCount((prevCount) => prevCount + 1);
            if (won === 'True') {
                toast.success(`'${player}' WON THE GAME\n\nPlay Again?`, {
                    icon: '👏',
                    position: "top-center"
                });
                setLock(true)
            }
            if (won === 'Draw'){
                toast.success(`There was a draw!\n\nPlay Again?`, {
                    position: "top-center"
                });
                setLock(true)
            }
        });

        return () => {
            // Clean up: Optionally leave the room if needed when component unmounts
            socket.emit('leave_game', { gameId });
            socket.off('load_board');
            socket.off('move_made');
        };
    }, []);

    const toggle = (index) => {
        console.log('Board button pressed');
        let player;
        if (lock || board[index]) {
            return;
        }
        player = count % 2 == 0 ? "X" : "O";
        setBoard(prevBoard => {
            const newBoard = [...prevBoard];
            newBoard[index] = player;
            return newBoard;
        });
        socket.emit('make_move', { 'game_id': gameId, 'index': index, 'player': player });
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
