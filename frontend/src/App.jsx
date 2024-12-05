import React , {useState} from 'react';
import { Routes, Route} from "react-router-dom";

import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Lobby from "./Components/Lobby/Lobby";
import GamePlay from "./Components/GamePlay/GamePlay";
import { Toaster } from 'react-hot-toast';
import { SocketProvider } from "./SocketProvider";
import { ApiProvider } from "./apiContext";

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeUsers, setActiveUsers] = useState([]);
  
  // allows users to navigate to different jsx pages and defines toast notification format
  return (
    <>
    
      <ApiProvider>
        <SocketProvider>
          <Routes>
              <Route path='/' element={<LoginSignup setCurrentUser={setCurrentUser} />} />
              <Route path='/lobby' element={<Lobby currentUser={currentUser} setCurrentUser={setCurrentUser} activeUsers={activeUsers} setActiveUsers={setActiveUsers}/>} />
              <Route path='/gameplay/:gameId' element={<GamePlay currentUser={currentUser} setCurrentUser={setCurrentUser} activeUsers={activeUsers} setActiveUsers={setActiveUsers}/>} />
          </Routes>
        </SocketProvider>
      </ApiProvider>
      <Toaster position="bottom-right" reverseOrder={false}/>
    </>
  )
};
