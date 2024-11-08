import React, { useEffect, useState, useContext } from 'react';
import axios from "axios";
import { toast } from 'react-hot-toast';
import { SocketContext } from '../../SocketProvider';

import './Lobby.css';

const Lobby = ({ currentUser }) => {
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
        toast( "Sending invite...",
            {
                duration: 6000,
            }
        );
        socket.emit('send_invite', { inviter: currentUser.userID, invitee });
    };

    useEffect(() => { getActiveUsers(); }, []); // Update the list of active users with every render of the page

    useEffect(() => {
        handleRegisterUser(); // register the currentUser with this socketID every time they enter the lobby
        
        socket.on('invite_recieved', (data) => {
            const inviter = data.userID;
            const invitee = data.invitee;
            const acceptInvite = window.confirm(`You have an invite from ${inviter}. Accept?`);
            const response = acceptInvite ? 'accepted' : 'declined';
            socket.emit('invite_response', { invitee, inviter, response });
        });

        socket.on('invite_accept', (data) => {
            console.log("Inside of invite_accept", data);
            // const inviter = data.inviter;
            // const invitee = data.invitee;
            // toast.success(`${invitee} has accepted your invite!`);
            // window.location.href = `/game/${inviter}/${invitee}`;
        });

        socket.on('invite_decline', (data) => {
            console.log("Inside of invite_decline", data);
            // const inviter = data.inviter;
            // const invitee = data.invitee;
            // toast.error(`${invitee} has declined your invite.`);
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
