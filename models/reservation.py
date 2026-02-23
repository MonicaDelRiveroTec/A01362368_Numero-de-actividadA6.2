"""Module for Reservation class with file-based persistence."""

import json
import os
from datetime import date

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'reservations.json')


def _load_reservations():
    """Load reservations from JSON file. Returns empty dict on error."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load reservations data: {e}")
        return {}


def _save_reservations(data):
    """Persist reservations dict to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"[ERROR] Failed to save reservations data: {e}")


class Reservation:
    """Links a Customer to a Hotel for a date range."""

    def __init__(self, reservation_id, customer_id, hotel_id,
                 check_in, check_out):
        self.reservation_id = str(reservation_id)
        self.customer_id = str(customer_id)
        self.hotel_id = str(hotel_id)
        self.check_in = str(check_in)
        self.check_out = str(check_out)
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
        res = cls(
            data['reservation_id'],
            data['customer_id'],
            data['hotel_id'],
            data['check_in'],
            data['check_out'],
        )
        res.status = data.get('status', 'active')
        return res

    @staticmethod
    def create(reservation_id, customer_id, hotel_id, check_in, check_out):
        """
        Create a reservation and update hotel room availability.

        Imports Hotel inline to avoid circular dependency issues.
        """
        from models.hotel import Hotel  # noqa: PLC0415

        reservations = _load_reservations()
        reservation_id = str(reservation_id)
        if reservation_id in reservations:
            print(f"[ERROR] Reservation '{reservation_id}' already exists.")
            return None

        success = Hotel.reserve_room(hotel_id, reservation_id)
        if not success:
            return None

        res = Reservation(reservation_id, customer_id, hotel_id,
                          check_in, check_out)
        reservations[reservation_id] = res.to_dict()
        _save_reservations(reservations)
        return res

    @staticmethod
    def cancel(reservation_id):
        """
        Cancel a reservation and restore hotel room availability.

        Imports Hotel inline to avoid circular dependency issues.
        """
        from models.hotel import Hotel  # noqa: PLC0415

        reservations = _load_reservations()
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
        _save_reservations(reservations)
        return True
    