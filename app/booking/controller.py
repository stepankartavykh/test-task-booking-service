"""Controller for booking domain."""
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.booking.model import Booking
from app.booking.schema import AllBookingsResponseSchema, BookingRequestSchema
from app.booking.service import BookingService
from app.users.controller import get_current_active_user
from app.users.schema import User

booking_router = APIRouter()

booking_service = BookingService()


@booking_router.post("/booking", status_code=201)
async def create_booking(booking: BookingRequestSchema,
                         current_user: Annotated[User, Depends(get_current_active_user)]):
    new_booking = Booking(
        who_booked=current_user.username,
        check_in_date=booking.check_in_date,
        check_out_date=booking.check_out_date,
        room_number=booking.room_number,
        purpose=booking.purpose
    )
    created_booking_id = booking_service.create_booking(new_booking)
    return {"createdId": created_booking_id}


@booking_router.get("/bookings", response_model=list[AllBookingsResponseSchema])
async def get_all_bookings(room_number: int = None, is_current_day: bool = False,
                           time_start: datetime = None, time_end: datetime = None):
    filters = {"room_number": room_number,
               "time_start": time_start,
               "time_end": time_end,
               "is_current_day": is_current_day}
    elements = booking_service.get_all_bookings(filters)
    return elements


@booking_router.get("/report")
async def get_bookings_report(room_number: int = None, is_current_day: bool = False,
                              time_start: datetime = None, time_end: datetime = None):
    filters = {"room_number": room_number,
               "time_start": time_start,
               "time_end": time_end,
               "is_current_day": is_current_day}
    data_for_report = booking_service.get_data_for_report(filters)
    report_path = booking_service.create_report(data_for_report, filters)
    media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    return FileResponse(report_path,
                        media_type=media_type,
                        filename="report.docx")
