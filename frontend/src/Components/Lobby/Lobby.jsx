import React, { useEffect, useState, useRef } from 'react';
import { toast } from 'react-hot-toast';
import './Lobby.css';
import UsersList from './UsersList';
import axios from "axios";

const Lobby = () => {
    const [activeUsers, setActiveUsers] = useState([]);

    // const confirmUserRegistration = () => {
    //     axios.post('http://127.0.0.1/register').then(response => {
    //         if (response.status === 201) {
    //             toast.success("User registered!");
    //             getActiveUsers();
    //         } else {
    //             toast.error("User not registered.");
    //         }
    //     }).catch(error => {
    //         toast.error("Error registering user.");
    //         if (error.response) {
    //             console.error('Error response data:', error.response.data);
    //             console.error('Error status:', error.response.status);
    //         } else if (error.request) {
    //             console.error('Error request:', error.request);
    //         } else {
    //             console.error('Error message:', error.message);
    //         }
    //     });
    // } // End confirmUserRegistration func

    const getActiveUsers = () => {
        axios.get('http://127.0.0.1/active_users').then(response => {
            console.log(response.data);
            if (response.status === 200) {
                console.log(response.data);
                setActiveUsers(response.data);
            } else {
                toast.error("Error getting active users.");
            }
        }).catch(error => {
            toast.error("Error getting active users.");
            if (error.response) {
                console.error('Error response data:', error.response.data);
                console.error('Error status:', error.response.status);
            } else if (error.request) {
                console.error('Error request:', error.request);
            } else {
                console.error('Error message:', error.message);
            }
        });
    }
    
    useEffect(() => { getActiveUsers(); }, []); // runs for each client

    return (
        <>
            <div>
                <h1 className="header">Welcome to the Lobby!</h1>
            </div>
            
        </>
    );
};

export default Lobby;