import React from "react";
import { useState } from 'react';
import { Product } from "../App";
import Update from "./update";
import { PlusCircle, Pencil, Trash2 } from "lucide-react";


interface HomeProps{
    data: Product[],
    fetch : Function,
    fetchError: string
}

function Home(props: HomeProps) {
    
    const data = props.data;
    const fetchProducts = props.fetch;
    const error = props.fetchError;

    

    // state for updating and adding new data
    const [updateProduct, setUpdateProduct] = useState<Product>(
        {id:null, product_name:"", product_category:"", quantity:0, unit_price:0}
        );
    
    const [update, setUpdate] = useState(false);
    const [request, setRequest] = useState("");

    // state for deleting data
    const [deleteId, setId] = useState<number|null>(null)


      
    const handleDelete = (id: number) => {
        fetch("http://localhost:8000/products/" + id, 
        {method : "DELETE"})
        .then(() => {
            console.log("Product deleted successfully!");
            toggleModal("close", id)
        }).then(() => {fetchProducts()})
        
        

    }

    const toggleUpdate = () => {
        setUpdate(!update);

    }

    const handleUpdate = (product: Product, request: string) => {

        if(request === "POST"){
            setRequest("POST");
        } else if(request === "PUT"){
            setRequest("PUT");
        }

        setUpdateProduct({id: product.id, product_name: product.product_name, product_category: product.product_category, unit_price: product.unit_price, quantity: product.quantity})

        toggleUpdate()



       
    }

    const toggleModal = (state: string, id: number) => {

        const modal = document.querySelector(".delete-dialog") as HTMLDialogElement;

        console.log(modal.getAttribute("open"))

        if(state === "open"){
            setId(id);
            modal.showModal();
            
        } else{
            setId(null)
            modal.close();
            
        }

    }

  return (
    <div className="table-wrapper">
        {update && <Update update = {toggleUpdate}
         productUpdated = {updateProduct} 
         request={request}
         refresh = {fetchProducts}/>}

        <dialog className="delete-dialog">
            <div>
                <p>Are you sure you want to delete this product from the table?</p>
                <div className="flex-btn">
                    <button className="cancel" onClick={() => {toggleModal("close", 0)}}>Cancel</button>
                    <button className="delete" onClick={() => handleDelete(deleteId as number)}>Delete</button>
                    
                </div>
            </div>
        </dialog>
       
        <div className="table-container">
            <table>
            <caption>List of Drinks Sold
                <button className="add-btn" 
                type="button" 
                onClick={() => {handleUpdate({id: null, product_name:"", product_category:"", quantity: 0, unit_price: 0}, "POST")}}>
                    <span className="label">Add Product</span>
                    <span className="icon"><PlusCircle /></span>
                </button>
            </caption>
            <thead>
                <tr>
                    <th>Drink</th>
                    <th>Category</th>
                    <th>Quantity</th>
                    <th>Unit Price (₦)</th>
                    <th></th>
                    <th></th>

                </tr>
            </thead>
            <tbody>
               
                {data.map((product: Product) =>(
                            <tr key={product.id} 
                            className={product.quantity === 0? "empty": "not-empty"}>
                                <td>{product.product_name}</td>
                                <td>{product.product_category}</td>
                                <td>{product.quantity}</td>
                                <td>{product.unit_price}</td>
                                <td className="update-btn">
                                    <button type="button" onClick={() => handleUpdate(product, "PUT")}>
                                        <span className="label">Update</span>
                                        <span className="icon"><Pencil /></span>
                                    </button>
                                </td>
                                <td className="delete-btn">
                                    <button type="button" onClick={() => {toggleModal("open", product.id as number)}}>
                                        <span className="label">Delete</span>
                                        <span className="icon"><Trash2 /></span>
                                    </button>
                                </td>
                               
                            </tr>
                            
                        ))}
                        
                    </tbody>
            </table>
            {error && <div className="fetch-error"> 
                        <p>Error: {error}</p>

                        <button className="refresh" onClick={() => {document.location.reload()}}>Refresh</button>
                    
                    </div>
            }
      </div>
      
    </div>
  )
}

export default Home
