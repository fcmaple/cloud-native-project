import React, { Component } from 'react'
import { BrowserRouter as Router, Route, Redirect, Switch } from 'react-router-dom'
import Content from "./Content"
import Login from './Login'
import Signup from './Signup'

class Main extends Component {
    constructor(props) {
        super(props)

        this.state = {
        }
    }

    render() {
        const { } = this.state
        return (
            <div className="main">
                {/* {islogin
                ?
                <Content
                    loginrole={loginrole}
                    memberdata={memberdata}
                    onLogout={this.onLogout}
                ></Content>
                :
                <Login
                    loginrole={loginrole}
                    memberdata={memberdata}
                    onChangeRole = {this.onChangeRole}
                    onsetMemberData = {this.onsetMemberData}
                ></Login>
                } */}
            </div>
        )
    }
}

export default Main;