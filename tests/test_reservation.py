"""Unit tests for the Reservation class."""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, mock_open

import models.reservation as reservation_module
import models.hotel as hotel_module
from models.reservation import Reservation
from models.hotel import Hotel


class TestReservationPersistence(unittest.TestCase):
    """Tests for _load_reservations and _save_reservations helpers."""

    def test_load_returns_empty_when_missing(self):
        with patch('os.path.exists', return_value=False):
            result = reservation_module._load_reservations()
        self.assertEqual(result, {})

    def test_load_handles_invalid_json(self):
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data='??')):
            result = reservation_module._load_reservations()
        self.assertEqual(result, {})

    def test_save_handles_io_error(self):
        with patch('builtins.open', side_effect=IOError("disk full")):
            reservation_module._save_reservations({})


class TestReservationCRUD(unittest.TestCase):
    """Tests for Reservation create and cancel."""

    HOTEL_FILE = '/tmp/test_res_hotels.json'
    RES_FILE = '/tmp/test_reservations.json'

    def setUp(self):
        self.h_patch = patch.object(hotel_module, 'DATA_FILE', self.HOTEL_FILE)
        self.r_patch = patch.object(reservation_module, 'DATA_FILE', self.RES_FILE)
        self.h_patch.start()
        self.r_patch.start()
        for f in (self.HOTEL_FILE, self.RES_FILE):
            if os.path.exists(f):
                os.remove(f)
        Hotel.create('H1', 'Test Hotel', 'NYC', 5)

    def tearDown(self):
        self.h_patch.stop()
        self.r_patch.stop()
        for f in (self.HOTEL_FILE, self.RES_FILE):
            if os.path.exists(f):
                os.remove(f)

    def test_create_reservation_success(self):
        r = Reservation.create('R1', 'C1', 'H1', '2025-01-01', '2025-01-05')
        self.assertIsNotNone(r)
        self.assertEqual(r.status, 'active')

    def test_create_reservation_duplicate(self):
        Reservation.create('R1', 'C1', 'H1', '2025-01-01', '2025-01-05')
        r2 = Reservation.create('R1', 'C2', 'H1', '2025-02-01', '2025-02-05')
        self.assertIsNone(r2)

    def test_create_reservation_hotel_not_found(self):
        r = Reservation.create('R2', 'C1', 'GHOST', '2025-01-01', '2025-01-05')
        self.assertIsNone(r)

    def test_cancel_reservation_success(self):
        Reservation.create('R3', 'C1', 'H1', '2025-03-01', '2025-03-05')
        result = Reservation.cancel('R3')
        self.assertTrue(result)

    def test_cancel_reservation_not_found(self):
        result = Reservation.cancel('GHOST')
        self.assertFalse(result)

    def test_cancel_reservation_already_cancelled(self):
        Reservation.create('R4', 'C1', 'H1', '2025-04-01', '2025-04-05')
        Reservation.cancel('R4')
        result = Reservation.cancel('R4')
        self.assertFalse(result)

    def test_create_reservation_no_rooms_available(self):
        Hotel.create('H_SMALL', 'Tiny', 'LA', 1)
        Reservation.create('R5', 'C1', 'H_SMALL', '2025-01-01', '2025-01-02')
        r2 = Reservation.create('R6', 'C2', 'H_SMALL', '2025-01-01', '2025-01-02')
        self.assertIsNone(r2)


if __name__ == '__main__':
    unittest.main()
