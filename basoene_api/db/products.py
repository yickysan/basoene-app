from sqlmodel import Session, select
from basoene_api.models.products import Products, ProductsPost, ProductUpdate

class ProductNotFoundError(Exception):
    ...


def db_products(session: Session) -> list[Products]: 

    query = select(Products)
    result = session.exec(query).all()
    return result


def db_get_product(product_name: str, session: Session) -> list[Products]:

    products = session.exec(
        select(Products).where(Products.product_name == product_name)
    ).all()

    if len(products) < 1:
        raise ProductNotFoundError("Product not found")
    
    return products


def db_add_product(product: ProductsPost, session: Session) -> Products:
    db_product = Products.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    
    return product


def db_update_product(id: int, product: ProductUpdate,session: Session) -> Products:
    
    db_product = session.get(Products, id)

    if not db_product:
       raise ProductNotFoundError("Product not found")

    updated_data = product.dict(exclude_unset=True)

    for k, v in updated_data.items():
        setattr(db_product, k, v)

    session.add(db_product)
    session.commit()
    session.refresh(db_product)

    return db_product


def db_delete_product(id: int, session: Session) -> None:
    
    product = session.get(Products, id)

    if not product:
        raise ProductNotFoundError("Product not found")
    
    session.delete(product)
    session.commit()
