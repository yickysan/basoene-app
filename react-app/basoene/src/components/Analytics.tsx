import React from "react"
import ProductStats from "./productStatistics";
import RoomStats from "./roomStatistics";

import { useState } from "react";


const Analytics = () => {
    // state to change the summary statistics
    const [summary, setSummary] = useState("");

    // state to change category for statistics
    const [category, setCategory] = useState("drinks");

    const toggleCategory = (category: string): void => {
        setCategory(category);
    }

    return (
        <div className="analytics">
            <div className="big-grid">
                <div className="controls">
                    <h2>Sales Performance</h2>
                    <div className="analysis-option">
                        <div className={`button-container ${category === "drinks"? "active":""}`} >
                            <button type="button" 
                            onClick={() => {toggleCategory("drinks")}}>
                                Drinks</button>
                        </div>
                        <div className={`button-container ${category === "rooms"? "active":""}`}>
                            <button type="button"
                            onClick={() => {toggleCategory("rooms")}}>
                                Rooms</button>
                        </div>
                        </div>
                        <div className="summary">
                            <div className="year">
                                <p tabIndex={0}>Year Summary</p>
                            </div>
                            <div className="month">
                                <p tabIndex={0}>Month Summary</p>
                            </div>
                            <div className="week">
                                <p tabIndex={0}>Week Summary</p>
                            </div>
                            <div className="today">
                                <p tabIndex={0}>Today</p>
                            </div>
                    </div>

                </div>
                {category === "drinks" && <ProductStats summary={summary}/>}
                {category === "rooms" && <RoomStats summary={summary}/>}
            </div>
            
        </div>
        
      );
 }
  
 export default Analytics;