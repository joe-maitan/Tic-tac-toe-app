import React, { useEffect, useState, useRef } from 'react';
import { io } from 'socket.io-client';
import { toast } from 'react-hot-toast';
import './Lobby.css';
import UsersList from './UsersList';

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState('');
    
    useEffect(() => {
        
    }, []); // Only run once on initial mount

    return (
        <>
            <div>
                <h1 className="header">Welcome to the Lobby!</h1>
            </div>
        </>
    );
};

export default Lobby;