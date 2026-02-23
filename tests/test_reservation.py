"""Unit tests for the Reservation class."""

import os
import unittest
from unittest.mock import patch

import models.reservation as reservation_module
import models.hotel as hotel_module
from models.reservation import Reservation, DateRange
from models.hotel import Hotel

HOTEL_FILE = '/tmp/test_res_hotels.json'
RES_FILE = '/tmp/test_reservations.json'


class TestDateRange(unittest.TestCase):
    """Tests for the DateRange helper class."""

    def setUp(self):
        """Print test description before each test."""
        print(f"\n▶  {self._testMethodName}: {self._testMethodDoc}")

    def test_date_range_stores_dates(self):
        """Should store check-in and check-out as string attributes."""
        dr = DateRange('2025-01-01', '2025-01-05')
        self.assertEqual(dr.check_in, '2025-01-01')
        self.assertEqual(dr.check_out, '2025-01-05')

    def test_date_range_repr(self):
        """Should return a readable string with both dates."""
        dr = DateRange('2025-01-01', '2025-01-05')
        self.assertIn('2025-01-01', repr(dr))
        self.assertIn('2025-01-05', repr(dr))

    def test_date_range_to_tuple(self):
        """Should return check-in and check-out as a tuple."""
        dr = DateRange('2025-01-01', '2025-01-05')
        self.assertEqual(dr.to_tuple(), ('2025-01-01', '2025-01-05'))


class TestReservationCRUD(unittest.TestCase):
    """Tests for Reservation create and cancel."""

    def setUp(self):
        """Print test description and set up hotel and reservation temp files."""
        print(f"\n▶  {self._testMethodName}: {self._testMethodDoc}")
        self.h_patch = patch.object(hotel_module, 'DATA_FILE', HOTEL_FILE)
        self.r_patch = patch.object(reservation_module, 'DATA_FILE', RES_FILE)
        self.h_patch.start()
        self.r_patch.start()
        for f in (HOTEL_FILE, RES_FILE):
            if os.path.exists(f):
                os.remove(f)
        Hotel.create('H1', 'Test Hotel', 'NYC', 5)

    def tearDown(self):
        """Stop patchers and clean up temp files after each test."""
        self.h_patch.stop()
        self.r_patch.stop()
        for f in (HOTEL_FILE, RES_FILE):
            if os.path.exists(f):
                os.remove(f)

    def test_create_reservation_success(self):
        """Should create a reservation with active status and return it."""
        r = Reservation.create('R1', 'C1', 'H1', '2025-01-01', '2025-01-05')
        self.assertIsNotNone(r)
        self.assertEqual(r.status, 'active')

    def test_create_reservation_duplicate(self):
        """Should return None and print error when reservation ID already exists."""
        Reservation.create('R1', 'C1', 'H1', '2025-01-01', '2025-01-05')
        r2 = Reservation.create('R1', 'C2', 'H1', '2025-02-01', '2025-02-05')
        self.assertIsNone(r2)

    def test_create_reservation_hotel_not_found(self):
        """Should return None when the referenced hotel does not exist."""
        r = Reservation.create('R2', 'C1', 'GHOST', '2025-01-01', '2025-01-05')
        self.assertIsNone(r)

    def test_cancel_reservation_success(self):
        """Should cancel an active reservation and return True."""
        Reservation.create('R3', 'C1', 'H1', '2025-03-01', '2025-03-05')
        result = Reservation.cancel('R3')
        self.assertTrue(result)

    def test_cancel_reservation_not_found(self):
        """Should return False and print error when reservation ID does not exist."""
        result = Reservation.cancel('GHOST')
        self.assertFalse(result)

    def test_cancel_reservation_already_cancelled(self):
        """Should return False and print error when reservation is already cancelled."""
        Reservation.create('R4', 'C1', 'H1', '2025-04-01', '2025-04-05')
        Reservation.cancel('R4')
        result = Reservation.cancel('R4')
        self.assertFalse(result)

    def test_create_reservation_no_rooms_available(self):
        """Should return None when the hotel has no available rooms left."""
        Hotel.create('H_SMALL', 'Tiny', 'LA', 1)
        Reservation.create('R5', 'C1', 'H_SMALL', '2025-01-01', '2025-01-02')
        r2 = Reservation.create('R6', 'C2', 'H_SMALL', '2025-01-01', '2025-01-02')
        self.assertIsNone(r2)

    def test_reservation_to_dict(self):
        """Should serialize a Reservation instance into a correct dictionary."""
        r = Reservation.create('R7', 'C1', 'H1', '2025-05-01', '2025-05-03')
        d = r.to_dict()
        self.assertEqual(d['reservation_id'], 'R7')
        self.assertEqual(d['status'], 'active')

    def test_reservation_from_dict(self):
        """Should deserialize a Reservation correctly from a dictionary."""
        r = Reservation.create('R8', 'C1', 'H1', '2025-06-01', '2025-06-03')
        d = r.to_dict()
        r2 = Reservation.from_dict(d)
        self.assertEqual(r2.customer_id, 'C1')
        self.assertEqual(r2.hotel_id, 'H1')


if __name__ == '__main__':
    unittest.main()
