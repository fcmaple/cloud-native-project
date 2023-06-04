import React, { Component, Children } from "react"

export default class Header extends Component {
    constructor(props) {
        super(props)

        this.state = {
        }
    }

    render() {
        const { islogin, children, title } = this.props
        return (
            <div className="header">
                {/* <div className="headerBtn"></div>*/}
                <div className="headerTitle">
                    <h3>{title}</h3>
                </div> 
                {children}
                {/* {this.onIslogin(islogin)} */}
            </div>
        )
    }
}