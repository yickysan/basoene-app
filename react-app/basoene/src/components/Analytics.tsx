import React from "react";
import {ChevronRightCircle, ChevronLeftCircle} from "lucide-react";
import ProductStats from "./productStatistics";
import RoomStats from "./roomStatistics";

import { useState } from "react";

type AnalyticsPage = {page: "drinks"|"rooms"}

const Analytics = () => {
    // state to change the summary statistics
    const [summary, setSummary] = useState("");

    // state to change category for statistics
    const [category, setCategory] = useState<AnalyticsPage>({page: "drinks"});

    const toggleCategory = (category: "drinks"|"rooms"): void => {
        setCategory({page: category});
    }

    const [mobileControlState, setMobileControlState] = useState(false);

    return (
        <div className="analytics">
            <button className={`control-btn ${mobileControlState? "open": ""}`} type="button"
            aria-label="anlysis options control button"
            onClick={() => {setMobileControlState(!mobileControlState)}}>
            {mobileControlState? <ChevronLeftCircle size={20}/> : <ChevronRightCircle size={20}/>}
            </button>
            <div className="big-grid">
                <div className="controls" data-open={mobileControlState}>
                    <h2>Sales Performance</h2>
                    <div className="analysis-option">
                        <div className={`button-container ${category.page === "drinks"? "active":""}`} >
                            <button type="button" 
                            onClick={() => {
                                toggleCategory("drinks"); 
                                setMobileControlState(!mobileControlState);
                                }
                                }>
                                Drinks</button>
                        </div>
                        <div className={`button-container ${category.page === "rooms"? "active":""}`}>
                            <button type="button"
                            onClick={() => {
                                toggleCategory("rooms");
                                setMobileControlState(!mobileControlState);
                                }
                                }>
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
                {category.page === "drinks" && <ProductStats summary={summary}/>}
                {category.page === "rooms" && <RoomStats summary={summary}/>}
            </div>
            
        </div>
        
      );
 }
  
 export default Analytics;