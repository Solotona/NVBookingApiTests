import pytest
import allure
from core.clients.endpoints import Endpoints
from core.clients.api_client import APIClient
from tests.conftest import create_booking


@allure.feature('Booking API')
@allure.story('Get booking by ID')
class TestGetBooking:

    @pytest.fixture(scope='class')
    def api_client(self):
        client = APIClient()
        yield client

    @allure.title('Get booking by ID')
    def test_get_booking_by_id(self, api_client, create_booking):
        booking_id = create_booking['booking_id']

        with allure.step(f'Get booking {booking_id}'):
            booking_data = api_client.get_booking_by_id(booking_id)