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

    /* getActiveUsers()
        @param None
        @brief When a user renders the lobby page. This request is sent to the server to get the 
        list of active users currrently in the system.
        @return None
    */
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
                // cookie.delete("currentUser", JSON.stringify(currentUser));
                // setCurrentUser(null);
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

    /* handleRegisterUser()
        @param None
        @brief When a user renders the lobby page we need to register their username with their socketID that is going
        to be sending requests such as invites and game moves. This is done here by grabbing the cookie in the system,
        then sending the username attacthed to the socketID to the backend.
        @return None
    */
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

    /* inviteUser()
        @param None
        @brief Handles logic of inviting a user.
        @return None
    */
    const inviteUser = (invitee) => {
        toast.success(`Sending invite to ${invitee}...`);
        socket.emit('send_invite', { inviter: currentUser.userID, invitee });
    };

    /* handleInvite()
        @param None
        @brief Handles the logic of accepting or declining the invite.
        @return None
    */
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

    useEffect(() => { 
        sessionStorage.setItem('isPageLoaded', 'true');
        getActiveUsers(); 
        handleRegisterUser();
    }, []);

    //listens for socket events of user joining, invited receieved, and the response to the invite
    useEffect(() => {
      const handleInvites = async () => {
        
        // await handleRegisterUser();
        
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

        const handleBeforeUnload = (e) => {
            sessionStorage.setItem('isClosing', 'true');
            setTimeout(() => { sessionStorage.removeItem('isClosing'); }, 100); // Slight delay to ensure the flag is cleared on refresh
            e.preventDefault();
            e.returnValue = "data will get lost";
        }; // End handleBeforeUnload

        const handleUnload = () => {
            if (sessionStorage.getItem('isClosing') === 'true') {
              navigator.sendBeacon(`${serverURL}${basePath}/logout`, '');
            }
        }; // End handleUnload

        window.addEventListener('beforeunload', handleBeforeUnload);
        window.addEventListener('unload', handleUnload);
        handleInvites();

        //if socket non-reponsive, it unmounts and closes all loose ends
        return () => {
            socket.off('user_joined');
            socket.off('invite_recieved');
            socket.off('handle_invite_response');
            socket.off('successful_registration');
            socket.off('game_created');
            socket.off('user_left');
            window.removeEventListener('beforeunload', handleBeforeUnload);
            window.removeEventListener('unload', handleUnload);
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
