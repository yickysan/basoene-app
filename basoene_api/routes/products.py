from fastapi import APIRouter
from fastapi import Response, Depends, HTTPException
from sqlmodel import Session, select
from typing import Generator
from basoene_api.models.products import Products, ProductsPost, engine

router = APIRouter()

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

@router.get("/products", response_model = list[Products])
async def products(session: Session = Depends(get_session)):
    
    query = select(Products)
    result = session.exec(query).all()
    return result


@router.get("/products/{product_name}/", response_model = list[Products])
async def get_product(product_name: str, response: Response, session: Session = Depends(get_session)):

    products = session.exec(
        select(Products).where(Products.product_name == product_name)
    ).all()

    if len(products) < 1:
        raise HTTPException(status_code=404, headers={"message": "Product not found"})
    
    return products
    
@router.post("/products", response_model = Products)
async def add_product(product: ProductsPost, session: Session = Depends(get_session)):
    db_product = Products.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return product


@router.put("/products/{id}", response_model = Products)
async def update_product(id: int, 
                   product: Products,
                   response: Response,
                   session: Session = Depends(get_session)):
    
    db_product = session.get(Products, id)

    if not db_product:
       raise HTTPException(status_code=404, headers={"message": "Product not found"})

    updated_data = product.dict(exclude_unset=True)

    for k, v in updated_data.items():
        setattr(db_product, k, v)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete("/products/{id}", response_model = str)
async def delete_product(id: int, 
                   response: Response,
                   session: Session = Depends(get_session)):
    
    product = session.get(Products, id)

    if not product:
        raise HTTPException(status_code=404, headers={"message": "Product not found"})
    
    session.delete(product)
    session.commit()

    return Response(status_code=200)

