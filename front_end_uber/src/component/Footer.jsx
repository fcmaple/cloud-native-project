import React, { Component, Children } from "react"

export default class Footer extends Component {
	render() {
		const { Cname, color, children } = this.props
		return (
			<div className="footer"
				style={{ backgroundColor:color }}
			>{Cname}{children}</div>
		)

	}
}