import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';

const SocketContext = createContext(null);

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children, currentUser }) => {
    const [socket, setSocket] = useState(null);

    useEffect(() => {

        if (currentUser != null && socket == null) {
            const newSocket = io('http://localhost:5000', { query: { userID: currentUser.userID } });
            setSocket(newSocket);
        }

        // socket.emit('connect_to_backend', () => { console.log('Connected to backend server'); });

        // socket.on('disconnect', () => {
        //     console.log('Disconnected from server');
        // }); 
        
        // return () => {
        //     socket.disconnect();
        // };

    }, [currentUser, socket]);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};
