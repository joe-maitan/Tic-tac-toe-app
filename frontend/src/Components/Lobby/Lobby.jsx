import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';
import { toast } from 'react-hot-toast';
import {global_username} from '../LoginSignup/LoginSignup.jsx'
import UsersList from './UsersList';
import './Lobby.css';

const username = global_username;

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState('');
    const username = global_username;
    const socket = io('http://0.0.0.0:5001');

    useEffect(() => {
        socket.on('connect', function() {
            console.log('connected!!!');
            socket.emit('user_join', username);
            toast.success(`${username} joined the lobby!`);
        });
    
        socket.on('disconnect', function() {
            socket.disconnect();
            toast.error(`${username} left the lobby!`);
        });
    
        socket.on('user_list_update', function(users) {
            setActiveUsers(activeUsers => [...activeUsers, users['users']['username']]);
        });

        // Cleanup the socket connection when the component unmounts
        // return () => {
        //     if (socket) {
        //     socket.disconnect();
        //     }
        // };
    }, []); // Only run once on initial mount

    return (
        <div>
            <h1 className="header">Welcome to the Lobby!</h1>
            {/* <ul>
                <UsersList users={activeUsers} />
            </ul> */}
            <h2>Does this work? {activeUsers}</h2>
        </div>
    );
};

export default Lobby;