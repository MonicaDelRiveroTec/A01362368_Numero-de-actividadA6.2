"""Unit tests for the Hotel class."""

import json
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, mock_open

import models.hotel as hotel_module
from models.hotel import Hotel


class TestHotelPersistence(unittest.TestCase):
    """Tests for _load_hotels and _save_hotels helpers."""

    def test_load_returns_empty_dict_when_file_missing(self):
        with patch('os.path.exists', return_value=False):
            result = hotel_module._load_hotels()
        self.assertEqual(result, {})

    def test_load_handles_invalid_json(self):
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data='NOT JSON')):
            result = hotel_module._load_hotels()
        self.assertEqual(result, {})

    def test_save_handles_io_error(self):
        with patch('builtins.open', side_effect=IOError("disk full")):
            # should not raise, just print error
            hotel_module._save_hotels({'h1': {}})


class TestHotelCRUD(unittest.TestCase):
    """Tests for Hotel create/delete/display/modify."""

    def setUp(self):
        """Patch DATA_FILE to use a temp in-memory store."""
        self.patcher = patch.object(hotel_module, 'DATA_FILE',
                                    '/tmp/test_hotels.json')
        self.patcher.start()
        # clean slate
        if os.path.exists('/tmp/test_hotels.json'):
            os.remove('/tmp/test_hotels.json')

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists('/tmp/test_hotels.json'):
            os.remove('/tmp/test_hotels.json')

    def test_create_hotel_success(self):
        h = Hotel.create('H1', 'Grand Inn', 'NYC', 50)
        self.assertIsNotNone(h)
        self.assertEqual(h.name, 'Grand Inn')
        self.assertEqual(h.available_rooms, 50)

    def test_create_hotel_duplicate(self):
        Hotel.create('H1', 'Grand Inn', 'NYC', 50)
        h2 = Hotel.create('H1', 'Other', 'LA', 10)
        self.assertIsNone(h2)

    def test_delete_hotel_success(self):
        Hotel.create('H2', 'Sea View', 'Miami', 20)
        result = Hotel.delete('H2')
        self.assertTrue(result)

    def test_delete_hotel_not_found(self):
        result = Hotel.delete('GHOST')
        self.assertFalse(result)

    def test_display_hotel(self):
        Hotel.create('H3', 'Mountain Lodge', 'Denver', 15)
        h = Hotel.display('H3')
        self.assertIsNotNone(h)
        self.assertEqual(h.location, 'Denver')

    def test_display_hotel_not_found(self):
        result = Hotel.display('GHOST')
        self.assertIsNone(result)

    def test_modify_hotel(self):
        Hotel.create('H4', 'Old Name', 'Chicago', 30)
        result = Hotel.modify('H4', name='New Name')
        self.assertTrue(result)

    def test_modify_hotel_not_found(self):
        result = Hotel.modify('GHOST', name='X')
        self.assertFalse(result)

    def test_modify_unknown_field(self):
        Hotel.create('H5', 'Inn', 'Austin', 10)
        # should not crash, unknown field is warned and skipped
        result = Hotel.modify('H5', color='blue')
        self.assertTrue(result)


class TestHotelRoomOperations(unittest.TestCase):
    """Tests for reserve_room and cancel_room."""

    def setUp(self):
        self.patcher = patch.object(hotel_module, 'DATA_FILE',
                                    '/tmp/test_hotels_rooms.json')
        self.patcher.start()
        if os.path.exists('/tmp/test_hotels_rooms.json'):
            os.remove('/tmp/test_hotels_rooms.json')
        Hotel.create('R1', 'Tiny Hotel', 'Boston', 2)

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists('/tmp/test_hotels_rooms.json'):
            os.remove('/tmp/test_hotels_rooms.json')

    def test_reserve_room_success(self):
        result = Hotel.reserve_room('R1', 'RES001')
        self.assertTrue(result)

    def test_reserve_room_no_availability(self):
        Hotel.reserve_room('R1', 'RES001')
        Hotel.reserve_room('R1', 'RES002')
        result = Hotel.reserve_room('R1', 'RES003')
        self.assertFalse(result)

    def test_cancel_room_success(self):
        Hotel.reserve_room('R1', 'RES001')
        result = Hotel.cancel_room('R1', 'RES001')
        self.assertTrue(result)

    def test_cancel_room_not_in_hotel(self):
        result = Hotel.cancel_room('R1', 'GHOST_RES')
        self.assertFalse(result)

    def test_reserve_room_hotel_not_found(self):
        result = Hotel.reserve_room('GHOST', 'RES001')
        self.assertFalse(result)

    def test_cancel_room_hotel_not_found(self):
        result = Hotel.cancel_room('GHOST', 'RES001')
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
