import ReactDOM from "react-dom/client";
import React , {useState} from 'react';
import { Routes, Route, Router } from "react-router-dom";

import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Lobby from "./Components/Lobby/Lobby";
import GamePlay from "./Components/GamePlay/GamePlay";
import { Toaster } from 'react-hot-toast';
import { SocketProvider } from "./SocketProvider";

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);

  return (
    <>
      <SocketProvider>
      <Routes>
        <Route path='/' element={<LoginSignup setCurrentUser={setCurrentUser} />} />
        <Route path='/lobby' element={<Lobby currentUser={currentUser}/>} />
        <Route path='/gameplay' element={<GamePlay />} />
      </Routes>
      </SocketProvider>
      <Toaster position="bottom-right" reverseOrder={false}/>
    </>
  )
};

export default App;
