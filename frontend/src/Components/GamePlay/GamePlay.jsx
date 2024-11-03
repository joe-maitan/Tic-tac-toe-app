import { useNavigate } from "react-router-dom";
import { useState } from 'react'
import './GamePlay.css';
import circle_pic from '../Images/circle.png'
import x_pic from '../Images/x.png'

let data = ["","","","","","","","",""]

const GamePlay = () => {

    let [count, setCount] = useState(0);
    let [lock, setLock] = useState(false);

    const toggle = (e, num) => {
        if (lock) {
            return 0;
        }
        if (count % 2 ==0) {
            e.target.innerHTML = `<img src='${x_pic}'>`;
            data[num] = "X";
            setCount(++count);
        }
        else {
            e.target.innerHTML = `<img src='${circle_pic}'>`;
            data[num] = "O";
            setCount(++count);
        }
    }

    return(
        <div className="CONTAINER">
            <h1 className="title">Play Game!</h1>
            <div className="board">
                <div className="row1">
                    <div className="boxes" onClick={(e) => {toggle(e,0)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,1)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,2)}}></div>
                </div>
                <div className="row2">
                    <div className="boxes" onClick={(e) => {toggle(e,3)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,4)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,5)}}></div>
                </div>
                <div className="row3">
                    <div className="boxes" onClick={(e) => {toggle(e,6)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,7)}}></div>
                    <div className="boxes" onClick={(e) => {toggle(e,8)}}></div>
                </div>
            </div>
        </div>
    )
};

export default GamePlay;
