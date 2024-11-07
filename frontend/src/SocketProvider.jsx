import { createContext, useContext, useState, useEffect } from "react";
import io from "socket.io-client";

const SocketContext = createContext();

export const SocketProvider = ({ children }) => {
    const [socket, setSocket] = useState(null);
    const [user, setUser] = useState(null); // Store username and socket ID

    useEffect(() => {
        const newSocket = io("http://localhost:5000"); // Server URL
        setSocket(newSocket);

        newSocket.on("registration_success", (data) => {
            console.log("Socket has registered successfully!", data);
            setUser({ username: data.username, socketId: data.socket_id });
        });

        return () => {
            newSocket.disconnect();
        };
    }, []);

    return (
        <SocketContext.Provider value={{ socket, user }}>
            {children}
        </SocketContext.Provider>
    );
};

export const useSocket = () => useContext(SocketContext);