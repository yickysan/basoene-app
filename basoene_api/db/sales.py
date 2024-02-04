from sqlmodel import Session, select
from basoene_api.models.products import ProductSales, Products, SalesPost, engine
from typing import Generator

class NoSalesError(Exception):
    ...


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


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