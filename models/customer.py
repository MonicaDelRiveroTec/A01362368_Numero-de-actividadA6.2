"""Module for Customer class with file-based persistence."""

import os
from models.persistence import load_data, save_data

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers.json')


class Customer:
    """Represents a customer with contact info."""

    def __init__(self, customer_id, name, email, phone):
        self.customer_id = str(customer_id)
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Serialize customer to dictionary."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize customer from dictionary."""
        return cls(
            data['customer_id'],
            data['name'],
            data['email'],
            data['phone'],
        )

    @staticmethod
    def create(customer_id, name, email, phone):
        """Create and persist a new customer."""
        customers = load_data(DATA_FILE)
        customer_id = str(customer_id)
        if customer_id in customers:
            print(f"[ERROR] Customer '{customer_id}' already exists.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer.to_dict()
        save_data(DATA_FILE, customers)
        return customer

    @staticmethod
    def delete(customer_id):
        """Delete a customer by ID."""
        customers = load_data(DATA_FILE)
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"[ERROR] Customer '{customer_id}' not found.")
            return False
        del customers[customer_id]
        save_data(DATA_FILE, customers)
        return True

    @staticmethod
    def display(customer_id):
        """Print customer information to console."""
        customers = load_data(DATA_FILE)
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"[ERROR] Customer '{customer_id}' not found.")
            return None
        data = customers[customer_id]
        print("--- Customer ---")
        for key, value in data.items():
            print(f"  {key}: {value}")
        return Customer.from_dict(data)

    @staticmethod
    def modify(customer_id, **kwargs):
        """Modify editable fields of an existing customer."""
        customers = load_data(DATA_FILE)
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"[ERROR] Customer '{customer_id}' not found.")
            return False
        allowed = {'name', 'email', 'phone'}
        for key, value in kwargs.items():
            if key in allowed:
                customers[customer_id][key] = value
            else:
                print(f"[WARN] Field '{key}' is not modifiable or unknown.")
        save_data(DATA_FILE, customers)
        return True
