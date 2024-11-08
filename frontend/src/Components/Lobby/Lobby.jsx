import React, { useEffect, useState } from 'react';
import axios from "axios";
import { toast } from 'react-hot-toast';
import { useSocket } from '../../SocketProvider';
import { currentUser } from '../LoginSignup/LoginSignup';

import './Lobby.css';

const Lobby = ({ currentUser }) => {
    const [activeUsers, setActiveUsers] = useState([]);
    const socket = useSocket();

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

    useEffect(() => { 
        getActiveUsers(); 
    }, []);

    const inviteUser = (invitee) => {
        toast( "Sending invite...",
            {
                duration: 6000,
            }
        );
        if (!socket) {
            toast.error("Socket not connected.");
            return;
        }
        socket.emit('send_invite', { userID: currentUser.userID, invitee });
    };
    
    useEffect(() => {
        if (!socket) return;

        socket.on('receive_invite', (data) => {
            const inviter = data.userID;
            const invitee = data.invitee;
            const acceptInvite = window.confirm(`You have an invite from ${inviter}. Accept?`);
            const response = acceptInvite ? 'accepted' : 'declined';
            socket.emit('respond_invite', { inviter, invitee: 'current_user_id', response });
        });

        // socket.on('invite_response', (data) => {
        //     // const { invitee, response } = data;
        //     // alert(`${invitee} has ${response} your invite.`);
        // });

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
