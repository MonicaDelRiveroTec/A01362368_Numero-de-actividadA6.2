"""Demo runner showing all operations for Hotel, Customer, Reservation."""

from models.hotel import Hotel
from models.customer import Customer
from models.reservation import Reservation


def main():
    """Run a demonstration of all system operations."""
    print("=== Hotels ===")
    Hotel.create('H1', 'Grand Plaza', 'New York', 10)
    Hotel.display('H1')
    Hotel.modify('H1', name='Grand Plaza Updated')
    Hotel.display('H1')

    print("\n=== Customers ===")
    Customer.create('C1', 'Alice Smith', 'alice@example.com', '555-0100')
    Customer.display('C1')
    Customer.modify('C1', phone='555-9999')

    print("\n=== Reservations ===")
    Reservation.create('RES1', 'C1', 'H1', '2025-06-01', '2025-06-05')
    Reservation.cancel('RES1')

    print("\n=== Cleanup ===")
    Hotel.delete('H1')
    Customer.delete('C1')


if __name__ == '__main__':
    main()
