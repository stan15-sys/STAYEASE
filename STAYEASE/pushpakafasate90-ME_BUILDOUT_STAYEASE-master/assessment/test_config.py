"""Test configuration and constants for the StayEase API tests"""

import uuid
from datetime import datetime, timedelta

# API Configuration
BASE_URL = "http://localhost:8081/api"
TIMEOUT = 5

# User test data with unique identifiers
CUSTOMER = {
    "email": f"customer.{uuid.uuid4()}@test.com",
    "password": "Test@123!",  # Meets password requirements
    "firstName": "Test",
    "lastName": "Customer"
}

MANAGER = {
    "email": f"manager.{uuid.uuid4()}@test.com",
    "password": "Manager@123!",
    "firstName": "Test",
    "lastName": "Manager",
    "role": "HOTEL_MANAGER"
}

ADMIN = {
    "email": f"admin.{uuid.uuid4()}@test.com",
    "password": "Admin@123!",
    "firstName": "Test",
    "lastName": "Admin",
    "role": "ADMIN"
}

# Hotel test data
HOTEL = {
    "name": f"Test Hotel {datetime.now().timestamp()}",
    "location": "Test Location",
    "description": "Test Description",
    "availableRooms": 10
}

HOTEL_WITH_LIMITED_ROOMS = {
    "name": f"Limited Rooms Hotel {datetime.now().timestamp()}",
    "location": "Test Location",
    "description": "Hotel with limited availability for testing",
    "totalRooms": 1,
    "availableRooms": 1
}

# Booking dates (tomorrow to three days later)
TOMORROW = datetime.now() + timedelta(days=1)
THREE_DAYS_LATER = datetime.now() + timedelta(days=3)

BOOKING = {
    "checkInDate": TOMORROW.strftime("%Y-%m-%d"),
    "checkOutDate": THREE_DAYS_LATER.strftime("%Y-%m-%d")
}

# Invalid input test data
INVALID_PASSWORD_USER = {
    "email": f"invalid.{uuid.uuid4()}@test.com",
    "password": "weak",  # Doesn't meet password requirements
    "firstName": "Test",
    "lastName": "Invalid"
}

INVALID_EMAIL_USER = {
    "email": "invalid-email",  # Incorrect email format
    "password": "Valid@123!",
    "firstName": "Test",
    "lastName": "Invalid"
}

# Error messages
NO_ROOMS_ERROR = "No rooms available"

# Headers template (will be populated with tokens during tests)
AUTH_HEADER = lambda token: {"Authorization": f"Bearer {token}"}