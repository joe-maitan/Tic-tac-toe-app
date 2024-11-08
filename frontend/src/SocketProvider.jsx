import React, { createContext, useContext, useEffect } from 'react';
import io from 'socket.io-client';

const SocketContext = createContext();

export const useSocket = () => useContext(SocketContext);

export const SocketProvider = ({ children }) => {
    const socket = io('http://127.0.0.1:5000');

    useEffect(() => {
        socket.emit('connect_to_backend', () => {
            console.log('Connected to server');
        });

        // socket.on('disconnect', () => {
        //     console.log('Disconnected from server');
        // }); 
        
        return () => {
            socket.disconnect();
        };
    }, [socket]);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};
