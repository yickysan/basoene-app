from pydantic import BaseModel
from datetime import date


class DateResults(BaseModel):
    booking_date: date
    revenue : int


class MonthResults(BaseModel):
    month: int
    revenue : int


class DayResults(BaseModel):
    day: int
    revenue : int


class RoomResults(BaseModel):
    room_name: str
    revenue : int


class HourCount(BaseModel):
    hour: int
    booking_count : int

class BookingSummary(BaseModel):
    total_revenue: int
    avg_daily_revenue: float
    total_bookings: int