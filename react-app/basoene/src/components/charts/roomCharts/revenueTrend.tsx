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
      },
      title: {
        display: true,
        text: "Revenue Trend",
      },
    },
  };
  
    type DateResult = {
      booking_date: string;
      revenue: number;
    }


const RevenueTrend = () => {

    const data = useFetchChartData("room/date").data;

    const chartData = {
        labels : data.map((value: DateResult) => (value.booking_date)),
        datasets: [{
            label: "Revenue (₦)",
            data: data.map((value: DateResult) => (value.revenue)),
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

export default RevenueTrend

