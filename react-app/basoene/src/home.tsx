import React from "react";
import { useEffect, useState } from 'react';
import Update from "./update";


type Product = {
    id : number | null;
    product_name: string | null;
    product_category: string | null;
    quantity: number | null;
    unit_price: number | null;
  
  }

function Home() {
    const [data, setData] = useState<Product[]>(
        [{id:null, product_name:null, product_category:null, quantity: null, unit_price: null}]
        )
    
    const [updateProduct, setUpdateProduct] = useState<Product>({id:null, product_name:null, product_category:null, quantity: null, unit_price: null})
    
    const [update, setUpdate] = useState(false)

    const [request, setRequest] = useState("")
    const [deleteId, setId] = useState<number|null>(null)

      const url: string = "http://127.0.0.1:8000/products"

      const fetchProducts = (): void => {
        fetch(url)
            .then(response => {
                if (!response.ok){
                    throw new Error("Could not get messages!")
                }
                return response.json();
            })
            .then(result => {
                setData(result);
            })
            .catch(error => {
               console.log(error)
            });

      }


      useEffect(() => {
        // const abortController = new AbortController();
        fetchProducts()
        
    }, []);

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

        if(state === "open"){
            setId(id);
            modal.showModal();
            document.body.style.overflowY = "hidden";
        } else{
            setId(null)
            modal.close();
            document.body.style.overflowY = "auto";
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
                    Add Product
                </button>
            </caption>
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Category</th>
                    <th>Quantity</th>
                    <th>Unit Price</th>
                    <th></th>
                    <th></th>

                </tr>
            </thead>
            <tbody>
                {data!.map((product: Product) =>(
                            <tr key={product.id}>
                                <td>{product.product_name}</td>
                                <td>{product.product_category}</td>
                                <td>{product.quantity}</td>
                                <td>{product.unit_price}</td>
                                <td className="update-btn">
                                    <button type="button" onClick={() => handleUpdate(product, "PUT")}>Update</button>
                                </td>
                                <td className="delete-btn">
                                    <button type="button" onClick={() => {toggleModal("open", product.id as number)}}>Delete</button>
                                </td>
                               
                            </tr>
                            
                        ))}
                        
                    </tbody>
            </table>
      </div>
      
    </div>
  )
}

export default Home
