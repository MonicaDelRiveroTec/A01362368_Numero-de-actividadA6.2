"""Module for Reservation class with file-based persistence."""

import os
from models.persistence import load_data, save_data
from models.hotel import Hotel

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'reservations.json')


class DateRange:
    """Represents a check-in and check-out date pair."""

    def __init__(self, check_in, check_out):
        self.check_in = str(check_in)
        self.check_out = str(check_out)

    def __repr__(self):
        """Return a readable string representation of the date range."""
        return f"DateRange(check_in={self.check_in}, check_out={self.check_out})"

    def to_tuple(self):
        """Return check-in and check-out as a tuple."""
        return (self.check_in, self.check_out)


class Reservation:
    """Links a Customer to a Hotel for a date range."""

    def __init__(self, reservation_id, customer_id, hotel_id, date_range):
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)
        self.check_in = date_range.check_in
        self.check_out = date_range.check_out
        self.status = 'active'

    def to_dict(self):
        """Serialize reservation to dictionary."""
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'hotel_id': self.hotel_id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize reservation from dictionary."""
        date_range = DateRange(data['check_in'], data['check_out'])
        res = cls(
            data['reservation_id'],
            data['customer_id'],
            data['hotel_id'],
            date_range,
        )
        res.status = data.get('status', 'active')
        return res

    @staticmethod
    def create(reservation_id, customer_id, hotel_id, check_in, check_out):
        """Create a reservation and update hotel room availability."""
        reservations = load_data(DATA_FILE)
        reservation_id = str(reservation_id)
        if reservation_id in reservations:
            print(f"[ERROR] Reservation '{reservation_id}' already exists.")
            return None

        if not Hotel.reserve_room(hotel_id, reservation_id):
            return None

        date_range = DateRange(check_in, check_out)
        res = Reservation(reservation_id, customer_id, hotel_id, date_range)
        reservations[reservation_id] = res.to_dict()
        save_data(DATA_FILE, reservations)
        return res

    @staticmethod
    def cancel(reservation_id):
        """Cancel a reservation and restore hotel room availability."""
        reservations = load_data(DATA_FILE)
        reservation_id = str(reservation_id)
        if reservation_id not in reservations:
            print(f"[ERROR] Reservation '{reservation_id}' not found.")
            return False

        data = reservations[reservation_id]
        if data['status'] == 'cancelled':
            print(f"[ERROR] Reservation '{reservation_id}' already cancelled.")
            return False

        Hotel.cancel_room(data['hotel_id'], reservation_id)
        reservations[reservation_id]['status'] = 'cancelled'
        save_data(DATA_FILE, reservations)
        return True
