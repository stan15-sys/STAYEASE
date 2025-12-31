#!/usr/bin/env python

from test_utils import APIClient, TestAssertions
from test_config import (
    CUSTOMER, MANAGER, ADMIN,
    HOTEL, HOTEL_WITH_LIMITED_ROOMS, BOOKING,
    INVALID_PASSWORD_USER, INVALID_EMAIL_USER,
    NO_ROOMS_ERROR, AUTH_HEADER
)
from test_runner import TestRunner
import uuid

client = APIClient()
assertions = TestAssertions()

# Global storage for test data
test_data = {
    "customer": dict(CUSTOMER),
    "manager": dict(MANAGER),
    "admin": dict(ADMIN),
    "hotel": None,
    "booking": None
}

# User Authentication & Registration Tests
def register_customer():
    """Register a new customer with default role when role not specified"""
    response = client.post("users/register", json=test_data["customer"])
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "token")
    test_data["customer"]["token"] = response.json()["token"]

def register_manager():
    """Register a hotel manager with specific role"""
    response = client.post("users/register", json=test_data["manager"])
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "token")
    test_data["manager"]["token"] = response.json()["token"]

def register_admin():
    """Register an admin with specific role"""
    response = client.post("users/register", json=test_data["admin"])
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "token")
    test_data["admin"]["token"] = response.json()["token"]

def reject_invalid_password():
    """Reject registration with invalid password format"""
    response = client.post("users/register", json=INVALID_PASSWORD_USER, expected_status=400)
    assertions.assert_status_code(response, 400)

def reject_invalid_email():
    """Reject registration with invalid email format"""
    response = client.post("users/register", json=INVALID_EMAIL_USER, expected_status=400)
    assertions.assert_status_code(response, 400)

def login_success():
    """Login successfully with valid credentials"""
    response = client.post("users/login", json={
        "email": test_data["customer"]["email"],
        "password": test_data["customer"]["password"]
    })
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "token")

def login_failure():
    """Fail login with invalid credentials"""
    response = client.post("users/login", json={
        "email": test_data["customer"]["email"],
        "password": "wrongpassword"
    }, expected_status=404)
    assertions.assert_status_code(response, 404)

# Hotel Management Tests
def view_hotels_publicly():
    """Allow public access to view hotels without authentication"""
    response = client.get("hotels")
    assertions.assert_status_code(response, 200)
    assertions.assert_json_type(response, list)

def create_hotel_as_admin():
    """Allow admin to create a hotel"""
    hotel_data = dict(HOTEL, name=f"Test Hotel {uuid.uuid4()}")
    response = client.post("hotels", json=hotel_data, 
                         headers=AUTH_HEADER(test_data['admin']['token']))
    assertions.assert_status_code(response, 200)
    test_data["hotel"] = response.json()

def create_hotel_as_manager_unauthorized():
    """Not allow manager to create a hotel"""
    response = client.post("hotels", json={
        "name": "Unauthorized Hotel",
        "location": "Test Location",
        "description": "Test Description",
        "availableRooms": 5
    }, headers=AUTH_HEADER(test_data['manager']['token']), expected_status=401)
    assertions.assert_status_code(response, 401)

def update_hotel_as_manager():
    """Allow manager to update hotel details"""
    response = client.put(f"hotels/{test_data['hotel']['id']}", json={
        "name": "Updated Hotel Name",
        "availableRooms": 15
    }, headers=AUTH_HEADER(test_data['manager']['token']))
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "name", "Updated Hotel Name")
    assertions.assert_json_field(response, "availableRooms", 15)

def admin_delete_hotel():
    """Allow admin to delete a hotel"""
    response = client.delete(f"hotels/{test_data['hotel']['id']}",
                           headers=AUTH_HEADER(test_data['admin']['token']))
    assertions.assert_status_code(response, 204)

def manager_delete_hotel_unauthorized():
    """Not allow manager to delete a hotel"""
    response = client.delete(f"hotels/{test_data['hotel']['id']}",
                           headers=AUTH_HEADER(test_data['manager']['token']),
                           expected_status=401)
    assertions.assert_status_code(response, 401)

# Booking Management Tests
def complete_booking_flow():
    """Complete the full booking flow"""
    # Create hotel with limited rooms
    response = client.post("hotels", json=HOTEL_WITH_LIMITED_ROOMS, 
                         headers=AUTH_HEADER(test_data['admin']['token']))
    assertions.assert_status_code(response, 200)
    test_data["hotel"] = response.json()
    
    # Book room as customer
    response = client.post(f"bookings/{test_data['hotel']['id']}", 
                         json=BOOKING,
                         headers=AUTH_HEADER(test_data['customer']['token']))
    assertions.assert_status_code(response, 200)
    test_data["booking"] = response.json()
    assertions.assert_json_field(response, "bookingId")

def no_rooms_available():
    """Not allow booking when no rooms available"""
    # Try to book the same hotel again (should be full)
    response = client.post(f"bookings/{test_data['hotel']['id']}", 
                         json=BOOKING,
                         headers=AUTH_HEADER(test_data['customer']['token']),
                         expected_status=404)
    
    if response.status_code == 404:
        assert NO_ROOMS_ERROR in response.text, \
            f"Expected '{NO_ROOMS_ERROR}' in response, got: {response.text}"
    else:
        assert False, f"API should return 404 when no rooms are available, got {response.status_code}"

def retrieve_booking_details():
    """Allow retrieving booking details"""
    booking_id = test_data["booking"]["bookingId"]
    response = client.get(f"bookings/{booking_id}",
                       headers=AUTH_HEADER(test_data['customer']['token']))
    assertions.assert_status_code(response, 200)
    assertions.assert_json_field(response, "bookingId", booking_id)

def manager_cancel_booking():
    """Allow manager to cancel booking"""
    booking_id = test_data["booking"]["bookingId"]
    response = client.delete(f"bookings/{booking_id}",
                          headers=AUTH_HEADER(test_data['manager']['token']))
    assertions.assert_status_code(response, 204)

def customer_cancel_booking_unauthorized():
    """Not allow customer to cancel booking"""
    booking_id = test_data["booking"]["bookingId"]
    response = client.delete(f"bookings/{booking_id}",
                          headers=AUTH_HEADER(test_data['customer']['token']),
                          expected_status=401)
    assertions.assert_status_code(response, 401)

# Test cases organized by category following the Cypress structure
tests = {
    "User Authentication & Registration": {
        "Register Customer": register_customer,
        "Register Hotel Manager": register_manager,
        "Register Admin": register_admin,
        "Reject Invalid Password": reject_invalid_password,
        "Reject Invalid Email": reject_invalid_email,
        "Login Successfully": login_success,
        "Fail Login with Invalid Credentials": login_failure
    },
    "Hotel Management": {
        "View Hotels Publicly": view_hotels_publicly,
        "Admin Create Hotel": create_hotel_as_admin,
        "Manager Cannot Create Hotel": create_hotel_as_manager_unauthorized,
        "Manager Update Hotel": update_hotel_as_manager,
        "Admin Delete Hotel": admin_delete_hotel,
        "Manager Cannot Delete Hotel": manager_delete_hotel_unauthorized
    },
    "Booking Management": {
        "Complete Booking Flow": complete_booking_flow,
        "No Rooms Available": no_rooms_available,
        "Retrieve Booking Details": retrieve_booking_details,
        "Manager Cancel Booking": manager_cancel_booking,
        "Customer Cannot Cancel Booking": customer_cancel_booking_unauthorized
    }
}

# Flatten the tests for the runner
flat_tests = {}
for category, category_tests in tests.items():
    for name, func in category_tests.items():
        flat_tests[name] = func

if __name__ == "__main__":
    TestRunner().run(flat_tests)