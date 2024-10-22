import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react'
import './App.css'

export default function App() {
  return (
    <div>
      <h1>TicTacToe.com</h1>
      <PlayOnline/>
      <PlayOffline/>
    </div>
  );
}; // End App() function
