import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';

  import { Line } from 'react-chartjs-2';
  import useFetchChartData from '../../../helper/fetchChartData';
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top" as const,
        display: false
      },
      title: {
        display: true,
        text: "Sales Trend",
      },
    },
  };
  
    type DateResult = {
      sale_date: string;
      total: number;
    }


const SalesTrend = () => {

    const data = useFetchChartData("product/date").data;

    const chartData = {
        labels : data.map((value: DateResult) => (value.sale_date)),
        datasets: [{
            label: "Sales (₦)",
            data: data.map((value: DateResult) => (value.total)),
            backgroundColor: "rgb(165, 80, 199)",
            borderColor : "rgb(165, 80, 199)"
        }]
    }

    return (
            <div className="chart-wrapper">
                <Line data={chartData} options={options}/>
            </div>
    )
}

export default SalesTrend

