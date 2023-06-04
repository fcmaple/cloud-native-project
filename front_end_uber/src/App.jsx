import React, { useState } from "react"
import {  Route, useNavigate, Routes } from 'react-router-dom'
import "./App.css"
import "./separator.css"
import "./lightbox.css"

import Login from "./component/Login"
import Signup from "./component/Signup"
import Passenger from './component/Passenger'
import Driver from './component/Driver'

const App = () => {
    const [islogin, setIsLogIn] = useState(false);
    const [loginrole, setlLogInRole] = useState("");
    const [accessToken, setAccessToken] = useState("");
    const [tokenType, setTokenType] = useState("");
    const navigate = useNavigate();

    const onChangeRole = (role) =>{
        console.log(role)
        setlLogInRole(role)
    }

    const onLogout = () => {
        setIsLogIn(false)
        setAccessToken("")
        setTokenType("")
        setlLogInRole("")
    }


    const onSetAccessToke = (data) => {

        const {tokenType,accessToken,role} = data

        setTokenType(tokenType)
        setAccessToken(accessToken)
        setlLogInRole(role)
        setIsLogIn(true)

        navigate(`/${role}`)
    }

    return (
        <div className="App">
            <Routes>
                <Route path='/login' element={<Login onSetAccessToke={onSetAccessToke}/>}></Route>
                <Route path='/signup' element={<Signup />}></Route>
                <Route path='/driver' element={<Driver tokenType={tokenType} accessToken={accessToken} loginrole={loginrole} onLogout={onLogout}/>}></Route>
                <Route path='/passenger' element={<Passenger tokenType={tokenType} accessToken={accessToken} loginrole={loginrole} onLogout={onLogout}/>}></Route>
                <Route index element={<Login onSetAccessToke={onSetAccessToke} />}></Route>
                <Route path='*' element={<Login onSetAccessToke={onSetAccessToke}/>}></Route>
            </Routes>
        </div>
    )

}

export default App;