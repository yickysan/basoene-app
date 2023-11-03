from pydantic import BaseModel
from datetime import date


class DateResults(BaseModel):
    sale_date: date
    total : int


class MonthResults(BaseModel):
    month: int
    total : int


class DayResults(BaseModel):
    day: int
    total : int


class ProductResults(BaseModel):
    product_name: str
    total : int


class HourResults(BaseModel):
    hour: int
    total : int

class SalesSummary(BaseModel):
    total_sales: int
    avg_daily_sales: float
    total_products_sold: int