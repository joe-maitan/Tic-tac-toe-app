import { useNavigate, useParams } from "react-router-dom";
import { useEffect, useState, useContext} from 'react';
import { SocketContext } from '../../SocketProvider';
import { toast } from 'react-hot-toast';
import axios from "axios";
import './GamePlay.css';
import circle_pic from '../Images/circle.png';
import x_pic from '../Images/x.png';
import { useApi } from '../../apiContext';
import cookie from '../utils/cookie';

//page for playing a game of tic tac toe
const GamePlay = ({ currentUser, setCurrentUser, activeUsers, setActiveUsers }) => {
    const [menuOpen, setMenuOpen] = useState(false);
    const { gameId } = useParams();
    let [count, setCount] = useState(0);
    let [lock, setLock] = useState(false);
    let [board, setBoard] = useState(Array(9).fill(""));

    const navigate = useNavigate();
    const socket = useContext(SocketContext);
    console.log(currentUser);

    const apiUrl = useApi();
    const toggleMenu = () => setMenuOpen(!menuOpen);

    /* playAgain()
        @param None
        @brief toast to notify players of a win or draw and quieries to play again
        @return response to the quiery of quit or play again
    */
    const playAgain = async (game_state) => {
        const won = game_state['won'];
        const player = game_state['player'];

        const response = await new Promise((resolve) => {
            var text = "";
        if (won === "True"){
            text = `${player} won the game!!`;
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

    /* handleLogout()
        @param None
        @brief When the user quits the page or clicks the Logout button, they send a request to logout
        of the server and are navigated to the main page.
        @return None
    */
    const handleLogout = () => {
        console.log("Logging out user " + currentUser.userID);
        socket.emit('logout_user', currentUser.userID);
        axios.post(apiUrl + '/logout', {"user_id": currentUser.userID})
        .then(response => {
            if (response.status === 200) {
                toast.success("Logged out!");
                console.log("Index of user logging out: " + activeUsers.indexOf(currentUser.userID));
                delete activeUsers[activeUsers.indexOf(currentUser.userID)];
                console.log("Active users after handleLogout: " + activeUsers);
                navigate('/');
            }
            console.log("Cookie after logging out: " + cookie);
            console.log("CurrentUser object after logging out: " + currentUser);
        }).catch(error => {
            toast.error("Error logging out. " + error.message)
            if (error.response) {
                console.error('Error response data:', error.response.data);
                console.error('Error status:', error.response.status);
            } else if (error.request) {
                console.error('Error request:', error.request);
            } else {
                console.error('Error message:', error.message);
            }
        });
    };

    useEffect(() => { 
        sessionStorage.setItem('isPageLoaded', 'true');
    }, []);

    //listens for socket events like joining a game or making a move
    useEffect(() => {
        socket.emit('join_game', { 'gameId': gameId, 'user': currentUser.userID });

        socket.on('load_board', (data) => {
            const board = data['board'];
            const currentUser = data['user'];
            setBoard(board);
            console.log(`current user: ${currentUser}`);
        });

        // updates the frontend board and handles play again or quit if game ends
        socket.on('move_made', async(data) =>{
            const index = data['index'];
            const player_symbol = data['player_symbol'];
            const player = data['player'];
            const won = data['game_state'];
            
            setBoard((prevBoard) => {
                const newBoard = [...prevBoard];
                newBoard[index] = player_symbol;
                return newBoard;
            });

            if (count == 0)
                setCount((prevCount) => prevCount + 1);
            if (won === 'True' || won === 'Draw') {
                setLock(true)
                const response = await playAgain({'won': won, 'player': player});
                if (response === "accepted") {
                    setBoard(Array(9).fill(""));
                    setLock(false);
                    setCount(0);
                    socket.emit('new_game', {'game_id' : gameId}); // create a new game instead of calling this method
                } else {
                    // socket.emit the opponent did not want to play again -> redirect other user to lobby
                    navigate('/lobby');
                }
            }
        });

        // notifies players if someone leaves while on the game play page
        socket.on('user_left', async(leftUser) => {
            console.log(`User left: ${leftUser}`);
            setActiveUsers((prevUsers) => prevUsers.filter((activeUsers) => activeUsers !== leftUser));
            if (leftUser != currentUser.userID) {
                toast.error(`${leftUser} disconnected from the server`);
            }
        });

        const handleBeforeUnload = (e) => {
            sessionStorage.setItem('isClosing', 'true');
            setTimeout(() => { sessionStorage.removeItem('isClosing'); }, 100); // Slight delay to ensure the flag is cleared on refresh
            e.preventDefault();
            e.returnValue = "data will get lost";
        }; // End handleBeforeUnload

        const handleUnload = () => {
            if (sessionStorage.getItem('isClosing') === 'true') {
              handleLogout();
            }
        }; // End handleUnload

        window.addEventListener('beforeunload', handleBeforeUnload);
        window.addEventListener('unload', handleUnload);

        return () => {
            socket.emit('leave_game', { gameId });
            socket.off('load_board');
            socket.off('move_made');
            socket.off('user_left');
            window.removeEventListener('beforeunload', handleBeforeUnload);
            window.removeEventListener('unload', handleUnload);
        };
    }, [socket]);

    //triggered when player presses a button on the tic tac toe board
    const toggle = (index) => {
        if (lock || board[index]) {
            return;
        }
        console.log('Board button pressed');
        socket.emit('make_move', {'game_id': gameId, 'index': index, 'player': currentUser.userID})
    } // End toggle func

    //returns the current game state
    return(
        <div className="CONTAINER">
            <nav className="navbar">
                <div className="menu-icon" onClick={toggleMenu}>
                    &#9776;
                </div>
                {menuOpen && (<ul className="menu">
                    <li><button onClick={handleLogout}>Logout</button></li>
                </ul>)}
            </nav>
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
