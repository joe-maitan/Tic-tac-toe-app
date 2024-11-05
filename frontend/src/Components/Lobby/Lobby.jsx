import React, { useEffect, useState, useRef } from 'react';
import { io } from 'socket.io-client';
import { toast } from 'react-hot-toast';
import './Lobby.css';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]); // Initialize state for the list of users
    const socketRef = useRef(null); // Ref to persist the socket instance across renders

    useEffect(() => {
        // Initialize socket connection only once, when the component is first mounted
        if (!socketRef.current) {
            socketRef.current = io('http://localhost:5000'); // Connect the socket to the backend server
            toast('Socket created', { duration: 2000 });
            console.log("Socket created");

            socketRef.current.on('connect', () => {
                console.log('Connected to server');
                
                socketRef.current.emit('new_user_connected', {
                    username: sessionStorage.getItem('username') 
                });

                toast("Welcome to the lobby! If you see someone you'd like to play with, click 'Invite' to start a game.", {
                    duration: 60000,
                });
            });

            // socketRef.current.on('user_list_update', (data) => {
            //     console.log('Active users:', data.users);
            //     setActiveUsers(data.users);
            // });
        } // End if statement

        // Cleanup the socket connection when the component is unmounted
        return () => {
            if (socketRef.current) {
                socketRef.current.disconnect();
                socketRef.current = null; // Set socket ref to null after disconnecting
            } // End if statement
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