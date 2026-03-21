import allure
import jsonschema

from conftest import booking_dates
from .schemas.booking_schema import BOOKING_SCHEMA
from pydantic import ValidationError
from core.models.booking import BookingResponse
from datetime import datetime
import pytest
from requests.exceptions import HTTPError



@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_random_data(api_client, generate_random_booking_data):
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
            assert response['booking']['additionalneeds'] == booking_data['additionalneeds'], "The additionalneeds does not match the expected"

    with allure.step('Verify schema validation'):
        jsonschema.validate(response, BOOKING_SCHEMA)


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    with allure.step("Send POST request to create booking with custom data"):
        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-09",
                "checkout": "2026-09-19"
            },
            "additionalneeds": "Dinner"
        }

        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

    with allure.step('Verify booking data matches request'):
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking without optional field "additionalneeds"')
def test_create_booking_without_optional_field_additionalneeds(api_client):
    with allure.step("Send POST request to create booking without optional field 'additionalneeds'"):
        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-08-15",
                "checkout": "2026-08-31"
            }
        }         # additionalneeds намеренно не передается

        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

    with allure.step('Verify booking data matches request'):
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == booking_data['totalprice']
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert 'additionalneeds' not in response['booking'], "Field 'additionalneeds' should not be present when not sent"


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with zero total price')
def test_create_booking_with_zero_total_price(api_client):
    with allure.step("Send POST request to create booking with zero total price"):
        booking_data = {
            "firstname": "Ivan",
            "lastname": "Ivanovich",
            "totalprice": 0,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-09-09",
                "checkout": "2026-09-19"
            },
            "additionalneeds": "Dinner"
        }

        response = api_client.create_booking(booking_data)
        try:
            BookingResponse(**response)
        except ValidationError as e:
            raise ValidationError(f"Response validation failed: {e}")

    with allure.step('Verify booking data matches request'):
        assert response['booking']['firstname'] == booking_data['firstname']
        assert response['booking']['lastname'] == booking_data['lastname']
        assert response['booking']['totalprice'] == 0
        assert response['booking']['depositpaid'] == booking_data['depositpaid']
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
        assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking without required field "last name"')
def test_create_booking_without_required_field_last_name(api_client):
    booking_data = {
        "firstname": "Ivan",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-09",
            "checkout": "2026-09-19"
        },
        "additionalneeds": "Dinner"
    }
    with allure.step("Send POST request to create booking without required field 'last name'"):
        with pytest.raises(HTTPError) as exception:
            response = api_client.create_booking(booking_data)
            response.raise_for_status()
        with allure.step(f"Verify status code"):
            status_code = exception.value.response.status_code
            assert status_code in [400, 500], f"Unexpected status code: {status_code}"