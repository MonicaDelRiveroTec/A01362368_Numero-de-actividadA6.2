# Hotel Reservation System

A Python application that manages hotels, customers, and reservations.

---

## Project Structure

```
a01362368_NumerodeActividadA6.2/
│
├── models/
│   ├── __init__.py
│   ├── persistence.py      # Shared load/save helpers for all models
│   ├── hotel.py            # Hotel class and CRUD operations
│   ├── customer.py         # Customer class and CRUD operations
│   └── reservation.py      # Reservation class + DateRange helper
│
├── tests/
│   ├── __init__.py
│   ├── base.py             # Shared base test class (BaseTempFileTest)
│   ├── test_hotel.py       # Unit tests for Hotel and persistence helpers
│   ├── test_customer.py    # Unit tests for Customer
│   └── test_reservation.py # Unit tests for Reservation and DateRange
│
├── main.py                 # Demo runner for all operations
├── conftest.py             # Adds project root to sys.path for test discovery
└── requirements.txt        # Dev dependencies (flake8, pylint, coverage)
```

---

## Requirements

- Python 3.8+
- No external runtime dependencies — standard library only
- Dev tools: `flake8`, `pylint`, `coverage`

Install dev tools:

```bash
pip install flake8 pylint coverage
```

---

## Running the Demo

From the project root:

```bash
python main.py
```

This demonstrates creating hotels, customers, and reservations, then cancelling and cleaning up.

---

## Running Tests

Always run from the **project root** using the `-m` flag:

```bash
python -m unittest discover -s tests -v
```

---

## Code Coverage

```bash
coverage run -m unittest discover -s tests
coverage report -m
```

Current coverage: **≥ 85%** across all modules.

---

## Static Analysis

### Flake8 (PEP8 style)

```bash
python -m flake8 models/ tests/ main.py --max-line-length=99
```

Expected output: silence (no warnings).

### Pylint

```bash
python -m pylint models/ tests/ main.py
```

Expected score: **10.00/10**

---

## Class Overview

### `Hotel`
Manages hotel data and room inventory.

| Method | Description |
|--------|-------------|
| `Hotel.create(id, name, location, rooms)` | Create and persist a new hotel |
| `Hotel.delete(id)` | Delete a hotel by ID |
| `Hotel.display(id)` | Print hotel info to console |
| `Hotel.modify(id, **kwargs)` | Update name, location, or total_rooms |
| `Hotel.reserve_room(hotel_id, reservation_id)` | Decrease available rooms |
| `Hotel.cancel_room(hotel_id, reservation_id)` | Restore available rooms |

### `Customer`
Manages customer contact information.

| Method | Description |
|--------|-------------|
| `Customer.create(id, name, email, phone)` | Create and persist a new customer |
| `Customer.delete(id)` | Delete a customer by ID |
| `Customer.display(id)` | Print customer info to console |
| `Customer.modify(id, **kwargs)` | Update name, email, or phone |

### `Reservation`
Links a customer to a hotel for a date range.

| Method | Description |
|--------|-------------|
| `Reservation.create(id, customer_id, hotel_id, check_in, check_out)` | Create reservation and reserve room |
| `Reservation.cancel(id)` | Cancel reservation and restore room |
