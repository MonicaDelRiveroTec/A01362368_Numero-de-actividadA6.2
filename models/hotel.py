"""Module for Hotel class with file-based persistence."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'hotels.json')


def _load_hotels():
    """Load hotels from JSON file. Returns empty dict on error."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load hotels data: {e}")
        return {}


def _save_hotels(data):
    """Persist hotels dict to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"[ERROR] Failed to save hotels data: {e}")


class Hotel:
    """Represents a hotel with rooms and reservation tracking."""

    def __init__(self, hotel_id, name, location, total_rooms):
        self.hotel_id = str(hotel_id)
        self.name = name
        self.location = location
        self.total_rooms = int(total_rooms)
        self.available_rooms = int(total_rooms)
        self.reservations = []

    def to_dict(self):
        """Serialize hotel to dictionary."""
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'location': self.location,
            'total_rooms': self.total_rooms,
            'available_rooms': self.available_rooms,
            'reservations': self.reservations,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize hotel from dictionary."""
        hotel = cls(
            data['hotel_id'],
            data['name'],
            data['location'],
            data['total_rooms'],
        )
        hotel.available_rooms = data.get('available_rooms', hotel.total_rooms)
        hotel.reservations = data.get('reservations', [])
        return hotel

    # ------------------------------------------------------------------ #
    # CRUD + business operations                                           #
    # ------------------------------------------------------------------ #

    @staticmethod
    def create(hotel_id, name, location, total_rooms):
        """Create and persist a new hotel."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' already exists.")
            return None
        hotel = Hotel(hotel_id, name, location, total_rooms)
        hotels[hotel_id] = hotel.to_dict()
        _save_hotels(hotels)
        return hotel

    @staticmethod
    def delete(hotel_id):
        """Delete a hotel by ID."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' not found.")
            return False
        del hotels[hotel_id]
        _save_hotels(hotels)
        return True

    @staticmethod
    def display(hotel_id):
        """Print hotel information to console."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' not found.")
            return None
        data = hotels[hotel_id]
        print(f"--- Hotel ---")
        for k, v in data.items():
            print(f"  {k}: {v}")
        return Hotel.from_dict(data)

    @staticmethod
    def modify(hotel_id, **kwargs):
        """Modify editable fields of an existing hotel."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' not found.")
            return False
        allowed = {'name', 'location', 'total_rooms'}
        for key, value in kwargs.items():
            if key in allowed:
                hotels[hotel_id][key] = value
            else:
                print(f"[WARN] Field '{key}' is not modifiable or unknown.")
        _save_hotels(hotels)
        return True

    @staticmethod
    def reserve_room(hotel_id, reservation_id):
        """Decrease available rooms and register reservation_id."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        if hotel_id not in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' not found.")
            return False
        if hotels[hotel_id]['available_rooms'] <= 0:
            print(f"[ERROR] No available rooms in hotel '{hotel_id}'.")
            return False
        hotels[hotel_id]['available_rooms'] -= 1
        hotels[hotel_id]['reservations'].append(str(reservation_id))
        _save_hotels(hotels)
        return True

    @staticmethod
    def cancel_room(hotel_id, reservation_id):
        """Increase available rooms and remove reservation_id."""
        hotels = _load_hotels()
        hotel_id = str(hotel_id)
        reservation_id = str(reservation_id)
        if hotel_id not in hotels:
            print(f"[ERROR] Hotel '{hotel_id}' not found.")
            return False
        if reservation_id not in hotels[hotel_id]['reservations']:
            print(f"[ERROR] Reservation '{reservation_id}' not in hotel.")
            return False
        hotels[hotel_id]['reservations'].remove(reservation_id)
        hotels[hotel_id]['available_rooms'] += 1
        _save_hotels(hotels)
        return True
