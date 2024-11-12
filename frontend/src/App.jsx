import ReactDOM from "react-dom/client";
import React , {useState} from 'react';
import { BrowserRouter, Routes, Route, Router } from "react-router-dom";

import './App.css'
import LoginSignup from "./components/LoginSignup/LoginSignup";
import Lobby from "./components/Lobby/Lobby";
import GamePlay from "./components/GamePlay/GamePlay";
import { Toaster } from 'react-hot-toast';
import { SocketProvider } from "./SocketProvider";

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    const userCookie = cookie.get('user');
    return userCookie ? JSON.parse(userCookie) : null;
  });

  const handleLogin = (userObject) => {
    setCurrentUser = userObject;
    cookie.set('user', JSON.stringify(userObject));
  }

  return (
    <>
      <SocketProvider>
        <BrowserRouter>
            <Route path='/login' element={<LoginSignup setCurrentUser={setCurrentUser} />} />
            <Route path='/lobby' element={<Lobby currentUser={currentUser} setCurrentUser={setCurrentUser}/>} />
            <Route path='/gameplay' element={<GamePlay />} />
        </BrowserRouter>
      
      </SocketProvider>
      <Toaster position="bottom-right" reverseOrder={false}/>
    </>
  )
};
