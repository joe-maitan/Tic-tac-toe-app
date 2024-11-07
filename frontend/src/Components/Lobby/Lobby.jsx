import React, { useEffect, useState, useRef } from 'react';
import { toast } from 'react-hot-toast';
import axios from "axios";

import './Lobby.css';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]);

    // const confirmUserRegistration = () => {
    //     axios.post('http://127.0.0.1:5000/register').then(response => {
    //         if (response.status === 201) {
    //             toast.success("User registered!");
    //             getActiveUsers();
    //         } else {
    //             toast.error("User not registered.");
    //         }
    //     }).catch(error => {
    //         toast.error("Error registering user.");
    //        
    //             console.error('Error response data:', error.response.data);
    //             console.error('Error status:', error.response.status);
    //         
    //             console.error('Error request:', error.request);
    //         
    //             console.error('Error message:', error.message);
    //         
    //     });
    // } // End confirmUserRegistration func

    const getActiveUsers = () => {
        axios.get('http://127.0.0.1:5000/active_users').then(response => {
            console.log(response.data);
            if (response.status === 200) {
                setActiveUsers(response.data.active_users);
            } 
        }).catch(error => {
            toast.error("Error getting active users.");
            console.error('Error response data:', error.response.data);
            console.error('Error status:', error.response.status);
            console.error('Error request:', error.request);
            console.error('Error message:', error.message);
        });
    } // End getActiveUsers func

    const inviteUser = (user) => {
        const inviter = ''; // try to use this to be the current user
        axios.post('http://127.0.0.1:5000/invite', { inviter, invitee })
        .then(response => {
            console.log(`Invite sent from ${inviter} to ${invitee}`);
            toast.success("Invite sent!");
        })
        .catch(error => {
            toast.error("Failed to send invite.");
            console.error('Error:', error);
        });
    } // End inviteUser func
    
    useEffect(() => { getActiveUsers(); }, []); // runs for each client

    return (
        <>
            <div>
                <h1 className="header">Welcome to the Lobby!</h1>
            </div>
    
            <div>
                <h1>Other Users</h1>
                <table>
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