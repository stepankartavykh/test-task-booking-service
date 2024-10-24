"""ORM model for booking entity in database."""
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app import Base


class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    who_booked = Column(String)
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    room_number = Column(Integer)
    purpose = Column(String)
