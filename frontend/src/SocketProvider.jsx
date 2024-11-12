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

        return () => newSocket.close();
    }, []);

    return (
        <SocketContext.Provider value={socket}>
            {children}
        </SocketContext.Provider>
    );
};

export {SocketContext, SocketProvider};