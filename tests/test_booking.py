import allure
import jsonschema
from .schemas.booking_schema import BOOKING_SCHEMA
from pydantic import ValidationError
from core.models.booking import BookingResponse



@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
@allure.title('Create booking with random data')
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
@allure.title('Create booking with custom data')
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
        assert response['booking']['firstname'] == booking_data['firstname'], "The firstname does not match the expected"
        assert response['booking']['lastname'] == booking_data['lastname'], "The lastname does not match the expected"
        assert response['booking']['totalprice'] == booking_data['totalprice'], "The totalprice does not match the expected"
        assert response['booking']['depositpaid'] == booking_data['depositpaid'], "The depositpaid does not match the expected"
        assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin'], "The date of checkin does not match the expected"
        assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout'], "The date of checkout does not match the expected"
        if response['booking'].get('additionalneeds'):
            assert response['booking']['additionalneeds'] == booking_data['additionalneeds'], "The additionalneeds does not match the expected"