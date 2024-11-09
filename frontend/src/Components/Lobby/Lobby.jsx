import React, { useEffect, useState, useContext } from 'react';
import axios from "axios";
import { toast } from 'react-hot-toast';
import { SocketContext } from '../../SocketProvider';

import './Lobby.css';

const Lobby = ({ currentUser, setCurrentUser }) => {
    const [activeUsers, setActiveUsers] = useState([]);
    const socket = useContext(SocketContext);

    const getActiveUsers = () => {
        axios.get('http://127.0.0.1:5000/active_users')
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

    const handleRegisterUser = () => {
        if (!currentUser) { // if the currentUser object is not intialized. grab it from sessionStorage
            setCurrentUser(sessionStorage.getItem("currentUser"));
        }

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

    const handleInvite = ({ invite, onAccept, onDecline }) => {
        const handleAccept = () => {
          onAccept(invite);
          const response = "accept";
          toast.dismiss(); // Close the toast
        };
      
        const handleDecline = () => {
          onDecline(invite);
          const response = "decline";
          toast.dismiss(); // Close the toast
        };

        socket.emit('invite_response', { invitee: currentUser.userID, inviter: invite.sender, response: response});
      
        return (
          <div>
            <p>You have received an invite from {invite.sender}</p>
            <button onClick={handleAccept}>Accept</button>
            <button onClick={handleDecline}>Decline</button>
          </div>
        );
      };

    useEffect(() => { getActiveUsers(); }, []); // Update the list of active users with every render of the page

    useEffect(() => {
        handleRegisterUser(); // register the currentUser with this socketID every time they enter the lobby/refresh the page
        
        socket.on('invite_recieved', (data) => {
            console.log("Inside of invite_recieved", data);
            response = handleInvite(data);
            // response = client input (accept/decline)
            // send response to inviter (socket.emit('invite_response', 
            // { invitee: currentUser.userID, inviter: data.inviter, response: response}));
        });

        socket.on('invite_response', (data) => {
            console.log("Inside of invite_response", data);
            
            // handle the accept/decline response
            // if (response === "accept") {
            //     // navigate to game
            // } else {
            //     // toast message that invite was declined
                    // keep the user in the lobby
            // }
        });

        return () => {
            if (socket) {
                socket.off('receive_invite');
                socket.off('invite_response');
            }
        };
    }, [socket]);

    return (
        <>
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
