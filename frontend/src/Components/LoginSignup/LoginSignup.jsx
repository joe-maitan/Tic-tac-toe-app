//import ReactDOM from "react-dom/client";
import { useNavigate } from "react-router-dom";
import { useState } from 'react'
import './LoginSignup.css'
//import Lobby from "../Lobby/Lobby";
import user_pic from '../Images/user.png'
import email_pic from '../Images/email.png'
import password_pic from '../Images/password.png'
import axios from "axios";
import { toast } from 'react-hot-toast';

export var global_username = "initial";

const LoginSignup = () => {
    console.log('LoginSignup component rendered');
    const [action, setAction] = useState('Login');
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLoginInput = (username, password) => {
      global_username = username;
        axios.post('http://127.0.0.1:5000/login', 
          {
          "username": username,
          "password": password
          }, {withCredentials: true})
          .then(response => {
            console.log('Response data:', response.data);
            console.log('Response status:', response.status);
            console.log('With credentials', {withCredentials: true});
            if (response.status === 201) {
              toast.success("Logged in!")
              navigate('/lobby');
            }
          })
          .catch(error => {
            toast.error("Error logging in. " + error.message)
            if (error.response) {
              console.error('Error response data:', error.response.data);
              console.error('Error status:', error.response.status);
            } else if (error.request) {
              console.error('Error request:', error.request);
            } else {
              console.error('Error message:', error.message);
            }
          });        
    } // End handleLoginInput

    const handleSignUpInput = (username, email, password) => {
      global_username = username;
        axios.post('http://127.0.0.1:5000/signup', 
          {
            "username": username,
            "email": email,
            "password": password
          }, {withCredentials: true}
        ).then(response => {
            console.log('Response data:', response.data);
            console.log('Response status:', response.status);
            if (response.status === 201) {
                toast.success("Account created successfully!");
                navigate('/lobby');
            } 
          })
          .catch(error => {
            toast.error("Sign In Error.");

            if (error.response) {
              console.error('Error response data:', error.response.data);
              console.error('Error status:', error.response.status);
            } else if (error.request) {
              console.error('Error request:', error.request);
            } else {
              console.error('Error message:', error.message);
            }
          });  
    } // End handleSignUpInput

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
  ); // End return statement
}; // End LoginSignup component 

export default LoginSignup;