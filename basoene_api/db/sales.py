from sqlmodel import Session, select
from basoene_api.models.products import ProductSales, Products, SalesPost
from datetime import date

class NoSalesError(Exception):
    ...


def db_sales(session: Session):
    query = select(Products.product_name, Products.unit_price, ProductSales).where(Products.id == ProductSales.product_id)
    result = session.exec(query).all()
    return result


def db_get_todays_sale(session: Session):
    sales = session.exec(
        (select(Products.product_name, Products.unit_price, ProductSales)
         .where(Products.id == ProductSales.product_id)
         .where(ProductSales.sale_date == date.today())
         .order_by(ProductSales.time.desc())
         )
    ).all()

    if len(sales) < 1:
        raise NoSalesError("No sales have been made today")

    return sales


def db_get_sales(date: str, session: Session):

    sales = session.exec(
        (select(Products.product_name, Products.unit_price, ProductSales)
         .where(Products.id == ProductSales.product_id)
         .where(ProductSales.sale_date == date)
         )
    ).all()

    if len(sales) < 1:
        raise NoSalesError("No sales have been made today")

    return sales


def db_add_sales(sales: SalesPost, session: Session):
    db_sales = ProductSales.from_orm(sales)
    session.add(db_sales)
    session.commit()
    session.refresh(db_sales)

    return db_sales
