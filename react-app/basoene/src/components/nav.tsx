import React from "react"
import { Link } from "react-router-dom"
import basoenelogo from"../images/basoenelogo.png"

const Nav = () => {
    return ( 
        
        <header>
            <picture className="logo">
                <img src={basoenelogo} alt="logo for basoene snug"></img>
           </picture>
            <nav className="navlist">
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/sales">Sales</Link></li>
                    <li><Link to="/rooms">Rooms</Link></li>
                    <li><Link to="/analytics">Analytics</Link></li>
                </ul>
            </nav>
        </header>
     );
}
 
export default Nav;