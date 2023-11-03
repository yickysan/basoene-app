import React, {useState, useEffect} from 'react';
import {Routes, Route} from "react-router-dom"
import './css/App.css';
import "./css/update.css"
import "./css/nav.css"
import "./css/sales.css"
import "./css/rooms.css"
import "./css/analytics.css"
import Home from "./components/home"
import Nav from './components/nav';
import SalesPage from './components/sales';
import Analytics from './components/Analytics';
import BookingPage from './components/booking';

export type Product = {
  id : number | null;
  product_name: string;
  product_category: string ;
  quantity: number ;
  unit_price: number ;

}


function App() {
  // states for fetching data
  const [data, setData] = useState<Product[]>(
  [{id:null, product_name:"", product_category:"", quantity:0, unit_price:0}]
  );

    const [error, setError] = useState<string|null>(null);

    const url: string = "http://127.0.0.1:8000/products"

    const fetchProducts = (): void => {

        fetch(url)
            .then(response => {
                if (!response.ok){
                    throw new Error("Could not get Products!")
                }
                return response.json();
            })
            .then(result => {
                setData(result);
            })
            .catch(error => {
               setError(error.message)
            });

      }


    useEffect(() => {
      fetchProducts()
      
  }, []);


  return (
    
      <div  className="App">
        <Nav/>
        <Routes> 
            <Route path="/" element=
              {<Home data={data} fetch={fetchProducts} fetchError={error as string}/>} />
            <Route path="/sales" element={<SalesPage data={data} fetch={fetchProducts}/>} />
            
            <Route path="/analytics" element={<Analytics/>} />
            <Route path="/rooms" element={<BookingPage/>} />
            
          </Routes>
      </div>
      
    
      
      
    
  );
}

export default App;
