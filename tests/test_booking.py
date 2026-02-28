import pytest
import allure
from faker import Faker
from datetime import datetime, timedelta
import jsonschema
from .schemas.booking_schema import BOOKING_SCHEMA


@allure.feature('Test booking')
@allure.story('Creating a new booking')
def test_create_booking(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data
    with allure.step("Send POST request to create booking"):
        response = api_client.create_booking(booking_data)

    with allure.step('Verify response status code is 200'):
        status_code = api_client.create_booking(booking_data)
        assert status_code == 200, f"Expected status 200 but got {response.status_code}"

    with allure.step('Verify schema validation'):
        jsonschema.validate(response, BOOKING_SCHEMA)