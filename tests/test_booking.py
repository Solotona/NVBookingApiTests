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

    with allure.step('Verify booking data matches request'):
        assert response['booking']['firstname'] == booking_data['firstname'], "The firstname does not match the expected"
        assert response['booking']['lastname'] == booking_data['lastname'], "The lastname does not match the expected"
        assert response['booking']['totalprice'] == booking_data['totalprice'], "The totalprice does not match the expected"
        assert response['booking']['depositpaid'] == booking_data['depositpaid'], "The depositpaid does not match the expected"
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "The date of checkin does not match the expected"
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "The date of checkout does not match the expected"
        if response['booking'].get('additionalneeds'):
            assert response['booking']('additionalneeds') == booking_data['additionalneeds'], "The additionalneeds does not match the expected"

    with allure.step('Verify schema validation'):
        jsonschema.validate(response, BOOKING_SCHEMA)