"""Unit tests for the Hotel class and shared persistence helpers."""

import os
import unittest
from unittest.mock import patch, mock_open

import models.hotel as hotel_module
from models.hotel import Hotel
from models.persistence import load_data, save_data
from tests.base import BaseTempFileTest

TEMP_FILE = '/tmp/test_hotels.json'
TEMP_ROOMS_FILE = '/tmp/test_hotels_rooms.json'


class TestPersistence(unittest.TestCase):
    """Tests for shared load_data and save_data helpers."""

    def setUp(self):
        """Print test description before each test."""
        print(f"\n▶  {self._testMethodName}: {self._testMethodDoc}")

    def test_load_returns_empty_dict_when_file_missing(self):
        """Should return empty dict when the JSON file does not exist."""
        with patch('os.path.exists', return_value=False):
            result = load_data('/fake/path.json')
        self.assertEqual(result, {})

    def test_load_handles_invalid_json(self):
        """Should return empty dict and print error when JSON is malformed."""
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data='NOT JSON')):
            result = load_data('/fake/path.json')
        self.assertEqual(result, {})

    def test_save_handles_io_error(self):
        """Should print error and not raise exception when file cannot be written."""
        with patch('builtins.open', side_effect=IOError("disk full")):
            save_data('/fake/path.json', {'h1': {}})


class TestHotelCRUD(BaseTempFileTest):
    """Tests for Hotel create, delete, display, and modify operations."""

    module = hotel_module
    temp_file = TEMP_FILE

    def test_create_hotel_success(self):
        """Should create a new hotel and persist it with correct attributes."""
        h = Hotel.create('H1', 'Grand Inn', 'NYC', 50)
        self.assertIsNotNone(h)
        self.assertEqual(h.name, 'Grand Inn')
        self.assertEqual(h.available_rooms, 50)

    def test_create_hotel_duplicate(self):
        """Should return None and print error when hotel ID already exists."""
        Hotel.create('H1', 'Grand Inn', 'NYC', 50)
        h2 = Hotel.create('H1', 'Other', 'LA', 10)
        self.assertIsNone(h2)

    def test_delete_hotel_success(self):
        """Should delete an existing hotel and return True."""
        Hotel.create('H2', 'Sea View', 'Miami', 20)
        result = Hotel.delete('H2')
        self.assertTrue(result)

    def test_delete_hotel_not_found(self):
        """Should return False and print error when hotel ID does not exist."""
        result = Hotel.delete('GHOST')
        self.assertFalse(result)

    def test_display_hotel(self):
        """Should print hotel info and return a Hotel instance with correct data."""
        Hotel.create('H3', 'Mountain Lodge', 'Denver', 15)
        h = Hotel.display('H3')
        self.assertIsNotNone(h)
        self.assertEqual(h.location, 'Denver')

    def test_display_hotel_not_found(self):
        """Should return None and print error when hotel ID does not exist."""
        result = Hotel.display('GHOST')
        self.assertIsNone(result)

    def test_modify_hotel(self):
        """Should update an allowed field on an existing hotel and return True."""
        Hotel.create('H4', 'Old Name', 'Chicago', 30)
        result = Hotel.modify('H4', name='New Name')
        self.assertTrue(result)

    def test_modify_hotel_not_found(self):
        """Should return False and print error when hotel ID does not exist."""
        result = Hotel.modify('GHOST', name='X')
        self.assertFalse(result)

    def test_modify_unknown_field(self):
        """Should warn and skip unknown fields without raising an exception."""
        Hotel.create('H5', 'Inn', 'Austin', 10)
        result = Hotel.modify('H5', color='blue')
        self.assertTrue(result)

    def test_from_dict_restores_hotel(self):
        """Should correctly reconstruct a Hotel instance from a dictionary."""
        Hotel.create('H6', 'Beach Resort', 'Cancun', 100)
        h = Hotel.display('H6')
        self.assertEqual(h.hotel_id, 'H6')
        self.assertEqual(h.total_rooms, 100)


class TestHotelRoomOperations(unittest.TestCase):
    """Tests for Hotel reserve_room and cancel_room operations."""

    def setUp(self):
        """Create a small hotel for room tests and print test description."""
        print(f"\n▶  {self._testMethodName}: {self._testMethodDoc}")
        self.patcher = patch.object(hotel_module, 'DATA_FILE', TEMP_ROOMS_FILE)
        self.patcher.start()
        if os.path.exists(TEMP_ROOMS_FILE):
            os.remove(TEMP_ROOMS_FILE)
        Hotel.create('R1', 'Tiny Hotel', 'Boston', 2)

    def tearDown(self):
        """Stop patcher and remove temp file after each test."""
        self.patcher.stop()
        if os.path.exists(TEMP_ROOMS_FILE):
            os.remove(TEMP_ROOMS_FILE)

    def test_reserve_room_success(self):
        """Should reserve a room, decrement availability, and return True."""
        result = Hotel.reserve_room('R1', 'RES001')
        self.assertTrue(result)

    def test_reserve_room_no_availability(self):
        """Should return False when all rooms are already reserved."""
        Hotel.reserve_room('R1', 'RES001')
        Hotel.reserve_room('R1', 'RES002')
        result = Hotel.reserve_room('R1', 'RES003')
        self.assertFalse(result)

    def test_cancel_room_success(self):
        """Should cancel a reservation, restore availability, and return True."""
        Hotel.reserve_room('R1', 'RES001')
        result = Hotel.cancel_room('R1', 'RES001')
        self.assertTrue(result)

    def test_cancel_room_not_in_hotel(self):
        """Should return False when reservation ID is not linked to the hotel."""
        result = Hotel.cancel_room('R1', 'GHOST_RES')
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        """Should return False and print error when hotel ID does not exist."""
        result = Hotel.reserve_room('GHOST', 'RES001')
        self.assertFalse(result)

    def test_cancel_room_hotel_not_found(self):
        """Should return False and print error when hotel ID does not exist."""
        result = Hotel.cancel_room('GHOST', 'RES001')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
