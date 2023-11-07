import React from "react"
import SalesTrend from "./charts/productCharts/salesTrend";
import SalesHour from "./charts/productCharts/hourlySales";
import SalesProduct from "./charts/productCharts/productSales";
import SalesDay from "./charts/productCharts/dailySales";
import {useFetchSalesSummary} from "../helper/fetchChartData";



interface statsProps{
    summary: string
}
const ProductStats = (props: statsProps) => {

    const summaryData = useFetchSalesSummary();
    const totalSales = new Intl.NumberFormat().format(summaryData.total_sales);
    const avgSales = new Intl.NumberFormat().format(summaryData.avg_daily_sales);


    return ( 
        <div className="stats">
            <div className="stat-title">
                <h3>Drink Sales Performance</h3>
                <div className="summary-card-wrapper">
                    <div className="summary-card">
                        <h5>Total Sales</h5>
                        <p>{`₦${totalSales}`}</p>
                    </div>
                    <div className="summary-card">
                        <h5>Avg Daily Sales</h5>
                        <p>{`₦${avgSales}`}</p>
                    </div>
                    <div className="summary-card">
                        <h5>Total Drinks Sold</h5>
                        <p>{summaryData.total_products_sold}</p>
                    </div>
                </div>
            </div>
             <div className="chart-grid">
                <SalesHour/>
                <SalesTrend/>
                <SalesProduct/>
                <SalesDay/>
            </div> 
        </div>
        
     );
}
 
export default ProductStats;