import React, { useEffect, useState, useContext } from 'react';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from 'react-hot-toast';
import { SocketContext } from '../../SocketProvider';
import { useApi } from '../../apiContext';

import cookie from '../utils/cookie';

import './Lobby.css';

const Lobby = ({ currentUser, setCurrentUser }) => {
    const [menuOpen, setMenuOpen] = useState(false);
    // const [dropdownOpen, setDropdownOpen] = useState(false);
    const [activeUsers, setActiveUsers] = useState([]);
    const navigate = useNavigate();

    const toggleMenu = () => setMenuOpen(!menuOpen);
    
    const socket = useContext(SocketContext);
    const apiUrl = useApi();

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
        axios.post(apiUrl + '/logout', {"user_id": currentUser.userID})
        .then(response => {
            if (response.status === 200) {
                toast.success("Logged out!");
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

    const inviteUser = (invitee) => {
        toast.success(`Sending invite to ${invitee}...`);
        socket.emit('send_invite', { inviter: currentUser.userID, invitee });
    };

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

    useEffect(() => {
      const registerUserAndHandleInvites = async () => {
        // TODO: Could move this to the above useEffect
        handleRegisterUser(); // register the currentUser with this socketID every time they enter the lobby/refresh the page
        
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
                navigate(`/gameplay/${data['game_id']}`);
            } else {
                toast.error(`${data['invitee']} declined ${data['inviter']}'s game request`);
            }
        });
      };

      registerUserAndHandleInvites();

        return () => {
            if (socket) {
                socket.off('receive_invite');
                socket.off('invite_response');
            }
        };
    }, [socket]);

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
