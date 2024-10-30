import React, { useEffect } from 'react';
import io from 'socket.io-client';
import './Lobby.css';

const Lobby = () => {
    // Initialize socket connection
    const socket = io('http://localhost:5000'); // Needs to be a socket connection to the backend server

    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to server');

            // Emit event to notify server of the new connection
            socket.emit('new_user_connected', { userId: 'USER_ID' }); // Replace with actual user ID if available
        });

        // Listen for server updates to the user list
        socket.on('user_list_update', (data) => {
            console.log('Active users:', data.users);
            // Update the lobby display as needed, e.g., with state
        });

        // Clean up socket connection on component unmount
        return () => {
            socket.disconnect();
        };
    }, [socket]); // UseEffect dependency ensures socket instance is only created once

    return (
        <div>
            <h1 className="header">LOBBY!</h1>
            {/* Here you could add a component to render the list of active users */}
        </div>
    );
};

export default Lobby;