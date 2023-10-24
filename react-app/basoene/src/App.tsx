import React from 'react';
import {BrowserRouter, Routes, Route} from "react-router-dom"
import './css/App.css';
import "./css/update.css"
import "./css/nav.css"
import Home from "./home"
import Nav from './nav';


function App() {

  return (
    <BrowserRouter>
      <div>
        <Nav/>
        <Routes> 
            <Route path="/" element={<Home/>} />
            {/* <Route path="/create" element={<Create/>} />
            <Route path="/messages/:id" element={<AffirmationDetails/>} /> */}
            
          </Routes>
      </div>
      
    </BrowserRouter>
    
      
      
    
  );
}

export default App;
