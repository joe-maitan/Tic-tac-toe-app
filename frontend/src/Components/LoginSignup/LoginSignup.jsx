//import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react'
import './LoginSignup.css'
import user_pic from '../Images/user.png'
import email_pic from '../Images/email.png'
import password_pic from '../Images/password.png'
import axios from "axios";

const LoginSignup = () => {
    const [action, setAction] = useState('Login');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLoginInput = (username, password) => {
        console.log(username, password);
        try {
            axios.post("http://127.0.0.1:5000/login", {
                'username': username, 'password': password
            })
        }
        catch(e) {
            console.log(e);
        }
    }

    const handleSignUpInput = (username, email, password) => {
        console.log(username, email, password);
        try {
            axios({
                method: 'POST',
                url: 'http://127.0.0.1:5000/signup',
                data : {'username': username, 'email': email, 'password': password},
                headers: {
                    'Content-Type': 'application/json'
                }
            })
        }
        catch(e) {
            console.log(e);
        }
    }

  return (
    <div className="container">
        <div className="header">
            <div className="text">{action}</div>
            <div className="underline"></div>
        </div>
    <div className="inputs">
        <div className="input" value={username} onChange={(e) => setUsername(e.target.value)}>
            <img src={user_pic} alt="" />
            <input type="text" required placeholder="Username"/>
        </div>
        {action==="Login"?<div></div>:<div className="input" value={email} onChange={(e) => setEmail(e.target.value)}>
            <img src={email_pic} alt="" />
            <input type="email" required placeholder="Email"/>
        </div>}
        <div className="input" value={password} onChange={(e) => setPassword(e.target.value)}>
            <img src={password_pic} alt="" />
            <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password"/>
        </div>
    </div>
    {action==="Login"?<div className="submit-sign-up">
        <div className="sign-up" onClick={()=>{setAction('Sign Up')}}><div className="sign-up">Don't have an account? <span>Click Here!</span></div></div>
    </div>:<div></div>}
    {action==="Login"?<div className={action==="Login"}></div>:<div className={action==="Sign Up"}></div>}
    {action==="Login"?<button className="button" onClick={()=>{handleLoginInput(username, password)}}>Login</button>:<button className="button" onClick={()=>{handleSignUpInput(username, email, password)}}>Sign Up</button>}
    </div>
  );
};

export default LoginSignup;