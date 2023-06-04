import React, {} from "react"

const Lightbox = (props) => {
    const { children, coverClick, title } = props
    return (
        <div className="lightbox">
            <div className="lightbox_cover" onClick={coverClick}></div>
            <div className="lightbox_content">
                <h4>{title}</h4>
                {children}
            </div>
        </div>
    )
}

export default Lightbox;