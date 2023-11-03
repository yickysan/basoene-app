import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from "chart.js";
  import { Bar } from "react-chartjs-2";
  import useFetchChartData from "../../../helper/fetchChartData";
  
  ChartJS.register(
      CategoryScale,
      LinearScale,
      BarElement,
      Title,
      Tooltip,
      Legend
    );
  
    export const options = {
      indexAxis: "y" as const,
      elements: {
        bar: {
          borderWidth: 2,
        },
      },
      responsive: true,
      plugins: {
        legend: {
          position: "right" as const,
        },
        title: {
          display: true,
          text: "Total Drink Sales",
        },
      },
    };
  
    type ProductResult = {
      product_name: string;
      total: number;
    }
  
   const SalesProduct = () => {
  
      const {data, isLoading, error} = useFetchChartData("product");
  
      const chartData = {
          labels : data.map((value: ProductResult) => (value.product_name)).reverse(),
          datasets: [{
              label: "Sales (₦)",
              data: data.map((value: ProductResult) => (value.total)).reverse(),
              backgroundColor: "rgb(165, 80, 199)",
              borderColor : "rgb(165, 80, 199)"
          }]
      }
  
      return (
          
              <div className="chart-wrapper product">
                  <Bar data={chartData} options={options}/>
              </div> 
        );
   }
    
   export default SalesProduct;