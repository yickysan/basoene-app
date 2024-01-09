import { useState} from "react"
import { Link } from "react-router-dom"
import {Menu, X } from "lucide-react"
import basoenelogo from"../images/basoenelogo.png"

type mobileNavState = {
    state: "open" | "close"
}

const Nav = () => {

    const [mobileNavState, setMobileNavState] = useState<mobileNavState>({state: "close"});

    const toggleMobileNav = () => {
        mobileNavState.state === "open"? setMobileNavState({state: "close"}) : setMobileNavState({state: "open"});
    }

    return ( 

        <header>
            <button type="button" 
            className="mobile-nav-toggle" 
            aria-label="Menu button"
            aria-controls="navlist"
            onClick={toggleMobileNav}>
                {mobileNavState.state === "open"? <X size={42}/> : <Menu size={42}/>} 
            </button>
            <picture className="logo">
                <img src={basoenelogo} alt="logo for basoene snug"></img>
           </picture>
            <nav className={`navlist ${mobileNavState.state}`} 
            aria-expanded={mobileNavState.state === "open"? "true" : "false"}>
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