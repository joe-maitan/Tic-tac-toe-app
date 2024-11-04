import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './Lobby.css';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]); // Initialize state for the list of users
    let socket; 

    useEffect(() => {
        if (!socket) {
            socket = io('http://localhost:5000'); // Ensures one client socket connection, per client
        }

        socket.on('connect', () => {
            console.log('Connected to server');

            // Emit event to notify server of the new connection
            socket.emit('new_user_connected', { userId: 'USER_ID' }); // Replace with actual user ID?
        });

        // Listen for server updates to the user list
        socket.on('user_list_update', (data) => {
            console.log('Active users:', data.users);  // Update the lobby display as needed, e.g., with state
           
        });

        // Cleanup the socket connection when the component is unmounted
        return () => {
            if (socket) {
                socket.disconnect();
            }
        };
    }, []); // UseEffect dependency ensures socket instance is only created once

    return (
        <div>
            <h1 className="header">Welcome to the Lobby!</h1>
            <ul>
                {activeUsers.map((user) => (
                    <li key={user.id}>{user.username}</li>
                ))}
            </ul>
        </div>
    );
};

export default Lobby;