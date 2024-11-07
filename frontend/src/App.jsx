import ReactDOM from "react-dom/client";
import React from 'react';
import { Routes, Route, Router } from "react-router-dom";
import { useState } from 'react'
import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Lobby from "./Components/Lobby/Lobby";
import GamePlay from "./Components/GamePlay/GamePlay";
import { Toaster } from 'react-hot-toast';
import { SocketProvider } from "./SocketProvider";

const App = () => {
  return (
    <>
      <Routes>
        <Route path='/' element={<LoginSignup />} />
        <Route path='/lobby' element={<Lobby />} />
        <Route path='/gameplay' element={<GamePlay />} />
      </Routes>
      <Toaster position="bottom-right" reverseOrder={false}/>
    </>
  )
};

export default App;
