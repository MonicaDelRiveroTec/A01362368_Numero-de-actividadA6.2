"""Module for Customer class with file-based persistence."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'customers.json')


def _load_customers():
    """Load customers from JSON file. Returns empty dict on error."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load customers data: {e}")
        return {}


def _save_customers(data):
    """Persist customers dict to JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"[ERROR] Failed to save customers data: {e}")


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
        customers = _load_customers()
        customer_id = str(customer_id)
        if customer_id in customers:
            print(f"[ERROR] Customer '{customer_id}' already exists.")
            return None
        customer = Customer(customer_id, name, email, phone)
        customers[customer_id] = customer.to_dict()
        _save_customers(customers)
        return customer

    @staticmethod
    def delete(customer_id):
        """Delete a customer by ID."""
        customers = _load_customers()
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"[ERROR] Customer '{customer_id}' not found.")
            return False
        del customers[customer_id]
        _save_customers(customers)
        return True

    @staticmethod
    def display(customer_id):
        """Print customer information to console."""
        customers = _load_customers()
        customer_id = str(customer_id)
        if customer_id not in customers:
            print(f"[ERROR] Customer '{customer_id}' not found.")
            return None
        data = customers[customer_id]
        print("--- Customer ---")
        for k, v in data.items():
            print(f"  {k}: {v}")
        return Customer.from_dict(data)

    @staticmethod
    def modify(customer_id, **kwargs):
        """Modify editable fields of an existing customer."""
        customers = _load_customers()
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
        _save_customers(customers)
        return True
