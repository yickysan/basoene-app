from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.products import Products, ProductsPost, ProductUpdate, engine
from basoene_api.db.products import (
    db_products,
    db_update_product,
    db_get_product,
    db_add_product,
    db_delete_product,
    ProductNotFoundError
)

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

@router.get("/products", response_model = list[Products])
async def products(session: Session = Depends(get_session)):
    
    return db_products(session)


@router.get("/products/{product_name}/", response_model = list[Products])
async def get_product(product_name: str, session: Session = Depends(get_session)):

    try:
        return db_get_product(product_name, session)

    except ProductNotFoundError:
        raise HTTPException(status_code=404, headers={"message": "Product not found"})
    
    
@router.post("/products", response_model = Products)
async def add_product(product: ProductsPost, session: Session = Depends(get_session)):

    return db_add_product(product, session)


@router.put("/products/{id}", response_model = Products)
async def update_product(id: int, 
                   product: ProductUpdate,
                   session: Session = Depends(get_session)):
    
    try:
        return db_update_product(id, product, session)

    except ProductNotFoundError:
       raise HTTPException(status_code=404, headers={"message": "Product not found"})

    


@router.delete("/products/{id}", response_model = str)
async def delete_product(id: int, 
                   response: Response,
                   session: Session = Depends(get_session)):
    
    try:
        db_delete_product(id, session)
        return Response(status_code=200)

    except ProductNotFoundError:
        raise HTTPException(status_code=404, headers={"message": "Product not found"})


