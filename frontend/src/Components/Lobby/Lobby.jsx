import React, { useEffect, useState, useContext } from 'react';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from 'react-hot-toast';
import { SocketContext } from '../../SocketProvider';
import { useApi } from '../../apiContext';

import cookie from '../utils/cookie';

import './Lobby.css';

//page for lobby
const Lobby = ({ currentUser, setCurrentUser }) => {
    const [menuOpen, setMenuOpen] = useState(false);
    const [activeUsers, setActiveUsers] = useState([]);
    const navigate = useNavigate();

    const toggleMenu = () => setMenuOpen(!menuOpen);
    
    const socket = useContext(SocketContext);
    const apiUrl = useApi();

    //returns the list of active users when called
    const getActiveUsers = () => {
        axios.get(apiUrl + '/active_users')
            .then(response => {
                if (response.status === 200) {
                    setActiveUsers(response.data.active_users);
                }
            })
            .catch(error => {
                toast.error("Error getting active users.");
                console.error('Error response data:', error.response?.data);
                console.error('Error status:', error.response?.status);
                console.error('Error request:', error.request);
                console.error('Error message:', error.message);
            });
    };

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
                cookie.delete("currentUser", JSON.stringify(currentUser));
                setCurrentUser(null);
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

    //registers or reregisters users when lobby page is rendered
    const handleRegisterUser = () => {
        if (!currentUser) {
            console.log("No currentUser found. Checking cookie");
            console.log("Information from grabbed cookie: " + cookie.get("currentUser"));
            currentUser = JSON.parse(cookie.get("currentUser"));
            setCurrentUser(currentUser);
        } else {
            console.log("currentUser found: " + currentUser.userID);
            console.log("Cookie: " + cookie.get("currentUser"));
        }

        console.log("Registering user " + currentUser.userID);
        socket.emit('register_user', {userID: currentUser.userID}); // Send a register event to the server

        socket.on('successful_registration', (data) => {
            if (data.success) {
                toast.success("Successfully registered with the server.");
            } else {
                toast.error("Failed to register with the server.");
            }
        }); // End socket on successful_registration event
    }; // End handleRegisterUser func

    //notifies the invitee that their invite it being sent
    const inviteUser = (invitee) => {
        toast.success(`Sending invite to ${invitee}...`);
        socket.emit('send_invite', { inviter: currentUser.userID, invitee });
    };

    //handles the invite response of acceptance or denial
    const handleInvite = async (invite) => {
        console.log(invite);
        const response = await new Promise((resolve) => {
        toast((t) => (
          <span>
            Invite received from {invite['inviter']}<br />  
            <button onClick={() => {
              resolve(handleAccept());
              toast.dismiss(t.id);
            }}
            style={{ margin: '8px 8px', padding: '4px 8px' }}>
              Accept
            </button>
            <button
            onClick={() => {
              toast.dismiss(t.id);
              resolve(handleDecline());
            }}
            style={{ margin: '8px 8px', padding: '4px 8px' }}>
            Decline
          </button>
          </span>
        ));

        const handleAccept = () => {
          return "accepted";
        };
      
        const handleDecline = () => {
          return "declined";
        };
    });
        return (
          response
        );
      };

    useEffect(() => { getActiveUsers(); }, []); // Update the list of active users with every render of the page

    //listens for socket events of user joinging, invited receieved, and the response to the invite
    useEffect(() => {
      const registerUserAndHandleInvites = async () => {
        
        await handleRegisterUser();
        
        socket.on('user_joined', async(newUser) => {
            console.log(`User joined: ${newUser}`);
            setActiveUsers((prevUsers) => {
                const uniqueUsers = new Set([...prevUsers, newUser]);
                return Array.from(uniqueUsers);
            });
        });

        socket.on('user_left', async(leftUser) => {
            console.log(`User left: ${leftUser}`);
            setActiveUsers((prevUsers) => prevUsers.filter((activeUsers) => activeUsers !== leftUser));
            if (leftUser != currentUser.userID) {
                toast.error(`${leftUser} disconnected from the server`);
            }
        });

        socket.on('invite_recieved', async(data) => {
            console.log("Inside of invite_recieved", data);
            const response = await handleInvite(data);
            console.log(response);
            socket.emit('invite_response', { invitee: currentUser.userID, inviter: data['inviter'], response: response});
        });

        socket.on('handle_invite_response', (data) => {
            console.log("Inside of invite_response", data);
            
            // handle the accept/decline response
            if (data["response"] === "accepted") {
                toast.success(`${data['invitee']} accepted ${data['inviter']}'s game request`);
                console.log("Navigating to /gameplay/" + data["game_id"]);
                socket.emit('create_game', {game_id: data['game_id'], player1: data['inviter'], player2: data['invitee']});
            } else {
                toast.error(`${data['invitee']} declined ${data['inviter']}'s game request`);
            }
        });

        socket.on('game_created', (data) => {
            console.log("Game created: ", data);
            navigate('/gameplay/' + data['game_id']);
        });
    };

      window.addEventListener('beforeunload', handleLogout);
      registerUserAndHandleInvites();

        //if socket non-reponsive, it unmounts and closes all loose ends
        return () => {
            // TODO: When a user refreshes the page it is not loving this at all
            socket.off('user_joined');
            socket.off('invite_recieved');
            socket.off('handle_invite_response');
            socket.off('successful_registration');
            socket.off('game_created');
            socket.off('user_left');
            window.removeEventListener('beforeunload', handleLogout);
        };
    }, [socket]);

    //returns the active users on the website
    return (
        <>
            <nav className="navbar">
                <div className="menu-icon" onClick={toggleMenu}>
                    &#9776;
                </div>
                {menuOpen && (<ul className="menu">
                    <li><button onClick={handleLogout}>Logout</button></li>
                </ul>)}
            </nav>
            <div>
                <h1 className="header">Welcome to the Lobby!</h1>
            </div>
    
            <div>
                <h2 className="header">Other Users</h2>
                <table className="userTable">
                    <thead>
                        <tr>
                            <th>Invite someone to play!</th>
                        </tr>
                    </thead>
                    <tbody>
                        {activeUsers.map((user, index) => (
                            <tr key={index}>
                                <td>{user}</td>
                                <td>
                                    <button onClick={() => inviteUser(user)}>Invite</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            
        </>
    );
};

export default Lobby;
