import React, { useEffect, useState } from 'react';
import { io }  from 'socket.io-client';
import { toast } from 'react-hot-toast';
import './Lobby.css';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]); // Initialize state for the list of users
    let socket; 

    useEffect(() => {
        if (socket == null) {
            socket = io('http://localhost:5000'); // Ensures one client socket connection, per client
            toast('Socket created', { duration: 2000 });
            console.log("Socket created");
        }

        socket.on('connect', (newUser) => {
            console.log('Connected to server');
            socket.emit(newUser['username'] + ' has connected');
            toast(
                "Welcome to the lobby! If you see someone you'd like to play with, click 'Invite' to start a game.",
                {
                  duration: 6000,
                }
              );
        });

        socket.on('user_list_update', (data) => {
            console.log('Active users:', data.users);  // Update the lobby display as needed, e.g., with state
            setActiveUsers(data.users);
        });

        // Cleanup the socket connection when the component is unmounted
        // return () => {
        //     if (socket) {
        //         socket.disconnect();
        //     }
        // };
    }, []); // UseEffect dependency ensures socket instance is only created once

    return (
        <div>
            <h1 className="header">Welcome to the Lobby!</h1>
            <ul>
                {activeUsers.map((user) => (
                    <li key={user.id}>{user.username}<button onSubmit>Invite</button></li>
                ))}
            </ul>
        </div>
    );
};

export default Lobby;