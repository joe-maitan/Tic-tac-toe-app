import ReactDOM from "react-dom/client";
import React , {useState} from 'react';
import { Routes, Route} from "react-router-dom";

import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Lobby from "./Components/Lobby/Lobby";
import GamePlay from "./Components/GamePlay/GamePlay";
import { Toaster } from 'react-hot-toast';
import { SocketProvider } from "./SocketProvider";
import { ApiProvider, useApi } from "./apiContext";

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);

  // const hostAddress = import.meta.env.VITE_FLASK_HOST;
  // const portNumber = import.meta.env.VITE_FLASK_SERVER_PORT;
  // const apiBaseUrl = `http://${hostAddress}:${portNumber}/api`;
  
  return (
    <>
    
      <ApiProvider>
      <p>API Base URL = {useApi()} </p>
        <SocketProvider>
          <Routes>
              <Route path='/' element={<LoginSignup setCurrentUser={setCurrentUser} />} />
              <Route path='/lobby' element={<Lobby currentUser={currentUser} setCurrentUser={setCurrentUser}/>} />
              <Route path='/gameplay' element={<GamePlay />} />
          </Routes>
        </SocketProvider>
      </ApiProvider>
      <Toaster position="bottom-right" reverseOrder={false}/>
    </>
  )
};
