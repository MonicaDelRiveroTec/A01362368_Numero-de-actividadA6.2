"""Unit tests for the Customer class."""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from unittest.mock import patch, mock_open

import models.customer as customer_module
from models.customer import Customer


class TestCustomerPersistence(unittest.TestCase):
    """Tests for _load_customers and _save_customers helpers."""

    def test_load_returns_empty_dict_when_file_missing(self):
        with patch('os.path.exists', return_value=False):
            result = customer_module._load_customers()
        self.assertEqual(result, {})

    def test_load_handles_invalid_json(self):
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', mock_open(read_data='BAD')):
            result = customer_module._load_customers()
        self.assertEqual(result, {})

    def test_save_handles_io_error(self):
        with patch('builtins.open', side_effect=IOError("no space")):
            customer_module._save_customers({'c1': {}})


class TestCustomerCRUD(unittest.TestCase):
    """Tests for Customer create/delete/display/modify."""

    def setUp(self):
        self.patcher = patch.object(customer_module, 'DATA_FILE',
                                    '/tmp/test_customers.json')
        self.patcher.start()
        if os.path.exists('/tmp/test_customers.json'):
            os.remove('/tmp/test_customers.json')

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists('/tmp/test_customers.json'):
            os.remove('/tmp/test_customers.json')

    def test_create_customer_success(self):
        c = Customer.create('C1', 'Alice', 'alice@x.com', '555-1234')
        self.assertIsNotNone(c)
        self.assertEqual(c.name, 'Alice')

    def test_create_customer_duplicate(self):
        Customer.create('C1', 'Alice', 'alice@x.com', '555-1234')
        c2 = Customer.create('C1', 'Bob', 'bob@x.com', '555-5678')
        self.assertIsNone(c2)

    def test_delete_customer_success(self):
        Customer.create('C2', 'Bob', 'bob@x.com', '555-0000')
        result = Customer.delete('C2')
        self.assertTrue(result)

    def test_delete_customer_not_found(self):
        result = Customer.delete('GHOST')
        self.assertFalse(result)

    def test_display_customer(self):
        Customer.create('C3', 'Carol', 'carol@x.com', '555-9999')
        c = Customer.display('C3')
        self.assertIsNotNone(c)
        self.assertEqual(c.email, 'carol@x.com')

    def test_display_customer_not_found(self):
        result = Customer.display('GHOST')
        self.assertIsNone(result)

    def test_modify_customer(self):
        Customer.create('C4', 'Dave', 'dave@x.com', '555-1111')
        result = Customer.modify('C4', email='new@x.com')
        self.assertTrue(result)

    def test_modify_customer_not_found(self):
        result = Customer.modify('GHOST', name='X')
        self.assertFalse(result)

    def test_modify_unknown_field(self):
        Customer.create('C5', 'Eve', 'eve@x.com', '555-2222')
        result = Customer.modify('C5', age=30)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
