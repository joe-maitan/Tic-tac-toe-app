import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react'
import './App.css'
import LoginSignup from "./Components/LoginSignup/LoginSignup";

export default function App() {
  return (
    <div>
      <h1 className="header">Tic Tac Toe!</h1>
      <LoginSignup/>
    </div>
  );
}; // End App() function
