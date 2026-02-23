"""Unit tests for the Customer class."""

import unittest

import models.customer as customer_module
from models.customer import Customer
from tests.base import BaseTempFileTest

TEMP_FILE = '/tmp/test_customers.json'


class TestCustomerCRUD(BaseTempFileTest):
    """Tests for Customer create, delete, display, and modify operations."""

    module = customer_module
    temp_file = TEMP_FILE

    def test_create_customer_success(self):
        """Should create a new customer and persist it with correct attributes."""
        c = Customer.create('C1', 'Alice', 'alice@x.com', '555-1234')
        self.assertIsNotNone(c)
        self.assertEqual(c.name, 'Alice')

    def test_create_customer_duplicate(self):
        """Should return None and print error when customer ID already exists."""
        Customer.create('C1', 'Alice', 'alice@x.com', '555-1234')
        c2 = Customer.create('C1', 'Bob', 'bob@x.com', '555-5678')
        self.assertIsNone(c2)

    def test_delete_customer_success(self):
        """Should delete an existing customer and return True."""
        Customer.create('C2', 'Bob', 'bob@x.com', '555-0000')
        result = Customer.delete('C2')
        self.assertTrue(result)

    def test_delete_customer_not_found(self):
        """Should return False and print error when customer ID does not exist."""
        result = Customer.delete('GHOST')
        self.assertFalse(result)

    def test_display_customer(self):
        """Should print customer info and return a Customer instance with correct data."""
        Customer.create('C3', 'Carol', 'carol@x.com', '555-9999')
        c = Customer.display('C3')
        self.assertIsNotNone(c)
        self.assertEqual(c.email, 'carol@x.com')

    def test_display_customer_not_found(self):
        """Should return None and print error when customer ID does not exist."""
        result = Customer.display('GHOST')
        self.assertIsNone(result)

    def test_modify_customer(self):
        """Should update an allowed field on an existing customer and return True."""
        Customer.create('C4', 'Dave', 'dave@x.com', '555-1111')
        result = Customer.modify('C4', email='new@x.com')
        self.assertTrue(result)

    def test_modify_customer_not_found(self):
        """Should return False and print error when customer ID does not exist."""
        result = Customer.modify('GHOST', name='X')
        self.assertFalse(result)

    def test_modify_unknown_field(self):
        """Should warn and skip unknown fields without raising an exception."""
        Customer.create('C5', 'Eve', 'eve@x.com', '555-2222')
        result = Customer.modify('C5', age=30)
        self.assertTrue(result)

    def test_from_dict_restores_customer(self):
        """Should correctly reconstruct a Customer instance from a dictionary."""
        Customer.create('C6', 'Frank', 'frank@x.com', '555-3333')
        c = Customer.display('C6')
        self.assertEqual(c.customer_id, 'C6')
        self.assertEqual(c.phone, '555-3333')


if __name__ == '__main__':
    unittest.main()
