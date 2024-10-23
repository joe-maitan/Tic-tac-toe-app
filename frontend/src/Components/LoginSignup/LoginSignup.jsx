import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react'
import './LoginSignup.css'
import user_pic from '../Images/user.png'
import email_pic from '../Images/email.png'
import password_pic from '../Images/password.png'

const LoginSignup = () => {
    const [action, setAction] = useState("Login");
  return (
    <div className="container">
        <div className="header">
            <div className="text">{action}</div>
            <div className="underline"></div>
        </div>
    <div className="inputs">
        <div className="input">
            <img src={user_pic} alt="" />
            <input type="text" placeholder="Username"/>
        </div>
        {action==="Login"?<div></div>:<div className="input">
            <img src={email_pic} alt="" />
            <input type="email" placeholder="Email"/>
        </div>}
        <div className="input">
            <img src={password_pic} alt="" />
            <input type="password" placeholder="Password"/>
        </div>
    </div>
    {action==="Login"?<div className="submit-sign-up">
        <div className="sign-up" onClick={()=>{setAction("Sign Up")}}><div className="sign-up">Don't have an account? <span>Click Here!</span></div></div>
    </div>:<div></div>}
    {action==="Login"?<div className="submit-container"><div className={action==="Login"?"submit":"submit gray"}>Login</div></div>:
    <div className="submit-container"><div className={action==="Sign Up"?"submit":"submit gray"}>Sign Up</div>
    </div>}
    </div>
  );
};

export default LoginSignup;