import { useState} from "react"
import { Link } from "react-router-dom"
import {Menu, X } from "lucide-react"
import basoenelogo from"../images/basoenelogo.png"
import SVGLogo from "./svgLogo"

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
                <SVGLogo />
           </picture>
            <nav className={`navlist ${mobileNavState.state}`} >
                <ul>
                    <li><Link onClick={toggleMobileNav} to="/">Home</Link></li>
                    <li><Link onClick={toggleMobileNav} to="/sales">Sales</Link></li>
                    <li><Link onClick={toggleMobileNav} to="/rooms">Rooms</Link></li>
                    <li><Link onClick={toggleMobileNav} to="/analytics">Analytics</Link></li>
                </ul>
            </nav>
        </header>
     );
}
 
export default Nav;