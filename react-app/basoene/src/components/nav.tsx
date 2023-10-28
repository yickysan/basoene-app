import React from "react"
import { Link } from "react-router-dom"
import basoene_logo from"../images/basoene_logo.png"

const Nav = () => {
    return ( 
        
        <header>
            <picture className="logo">
                <img src={basoene_logo} alt="logo for basoene snug"></img>
           </picture>
            <nav className="navlist">
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/sales">Sales</Link></li>
                    <li><Link to="/rooms">Rooms</Link></li>
                    <li><Link to="/bookings">Bookings</Link></li>
                </ul>
            </nav>
        </header>
     );
}
 
export default Nav;