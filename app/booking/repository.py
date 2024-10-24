"""Module for interaction with database."""
import datetime

from sqlalchemy import between, func, or_

from app import DBSession
from app.booking.model import Booking


class BookingRepository:

    def __init__(self):
        self.session_maker = DBSession

    def create_new_booking(self, booking) -> int:
        """Write booking to database."""
        with self.session_maker() as session:
            session.add(booking)
            session.commit()
            return booking.id

    def get_occupied_rooms_count(self, room_id: int, check_in_date: datetime, check_out_date: datetime) -> int:
        """Calculate how many rooms are busy in period."""
        with self.session_maker() as session:
            query = session.query(func.count(Booking.id))\
                .filter(Booking.room_number == room_id)\
                .filter(or_(between(Booking.check_in_date, check_in_date, check_out_date),
                            between(Booking.check_out_date, check_in_date, check_out_date)))
            count = query.scalar()
        return count

    def get_booking(self, booking_id: int) -> Booking | None:
        """Returns booking found by id."""
        with self.session_maker() as session:
            return session.query(Booking).filter(Booking.id == booking_id).one_or_none()

    def get_all_bookings(self, filters) -> list[Booking]:
        """All filtered bookings."""
        with self.session_maker() as session:
            query = session.query(Booking)
            room_number = filters.get('room_number')
            time_start = filters.get('time_start')
            time_end = filters.get('time_end')
            is_current_day = filters.get('is_current_day')
            start_day = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_day = datetime.datetime.now() + datetime.timedelta(days=1)
            end_day = end_day.replace(hour=0, minute=0, second=0, microsecond=0)
            if is_current_day:
                query = query.filter(or_(between(Booking.check_in_date, start_day, end_day),
                                         between(Booking.check_out_date, start_day, end_day)))
            if room_number is not None:
                query = query.filter(Booking.room_number == room_number).order_by(Booking.check_in_date)
            if time_start:
                query = query.filter(Booking.check_in_date > time_start)
            if time_end:
                query = query.filter(Booking.check_out_date < time_end)
            return query.all()

    def delete_booking(self, booking_id) -> None:
        with self.session_maker() as session:
            booking = session.get(Booking, booking_id)
            if booking:
                session.delete(booking)
                session.commit()

    def get_report_data(self, filters) -> list[Booking]:
        """Collect filtered data."""
        return self.get_all_bookings(filters)
