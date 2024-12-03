import React, { createContext, useContext, useEffect, useState } from 'react';
import io from 'socket.io-client';
import { useApi } from './apiContext';

const SocketContext = createContext(null);

const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const apiUrl = useApi();

    useEffect(() => {
        const newSocket = io(apiUrl);
        setSocket(newSocket);

        return () => {
            newSocket.close();
            setSocket(null); // Explicitly set socket to null on cleanup
        };
    }, [apiUrl]); // Include dependencies if apiUrl can change

    return (
        <SocketContext.Provider value={socket}>
            {socket ? children : <div>Connecting...</div>} {/* Graceful fallback */}
        </SocketContext.Provider>
    );
};

export { SocketContext, SocketProvider };
