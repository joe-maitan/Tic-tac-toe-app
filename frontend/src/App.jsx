import ReactDOM from "react-dom/client";
import React from 'react';
import { Routes, Route, Router } from "react-router-dom";
import { useState } from 'react'
import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";
import Lobby from "./Components/Lobby/Lobby";

const App = () => {
  return(
    <Routes>
      <Route path='/' element={<LoginSignup />} />
      <Route path='/lobby' element={<Lobby />} />
    </Routes>
  )
};

export default App;
