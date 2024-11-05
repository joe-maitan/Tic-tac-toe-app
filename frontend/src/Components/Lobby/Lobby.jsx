import React, { useEffect, useState, useRef } from 'react';
import { io } from 'socket.io-client';
import { toast } from 'react-hot-toast';
import './Lobby.css';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]); // Initialize state for the list of users
    const socketRef = useRef(null); // Ref to persist the socket instance across renders

    useEffect(() => {
        // Create a new socket connection
        socketRef.current = io('http://localhost:5000');

        // Listen for the 'activeUsers' event and update the state
        // socketRef.current.on('activeUsers', (users) => {
        //     setActiveUsers(users);
        // });

        // Listen for the 'userJoined' event and show a toast notification
        socketRef.current.on('connect', (username) => {
            toast.success(`${username} joined the lobby!`);
        });

        // Listen for the 'userLeft' event and show a toast notification
        socketRef.current.on('disconnect', (username) => {
            toast.error(`${username} left the lobby!`);
        });

        // Cleanup the socket connection when the component unmounts
        return () => {
            if (socketRef.current) {
            socketRef.current.disconnect();
            }
        };
    }, []); // Only run once on initial mount

    return (
        <div>
            <h1 className="header">Welcome to the Lobby!</h1>
            <ul>
                {activeUsers.map((user) => (
                    <li key={user.id}>{user.username} <button>Invite</button></li>
                ))}
            </ul>
        </div>
    );
};

export default Lobby;