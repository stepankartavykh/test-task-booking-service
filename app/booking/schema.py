"""Schemas for data validation."""
from datetime import datetime

from pydantic import BaseModel


class BookingRequestSchema(BaseModel):
    check_in_date: datetime
    check_out_date: datetime
    room_number: int
    purpose: str


class BookingResponseSchema(BaseModel):
    who_booked: str
    check_in_date: datetime
    check_out_date: datetime
    room_number: int


class AllBookingsFiltersSchema(BaseModel):
    room_number: int
    time_start: datetime | None
    time_end: datetime | None


class AllBookingsResponseSchema(BaseModel):
    who_booked: str
    check_in_date: datetime
    check_out_date: datetime
    room_number: int
    is_empty_now: bool | None
