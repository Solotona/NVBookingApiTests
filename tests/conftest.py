import requests
import pytest
import time
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts
from core.clients.api_client import APIClient

@pytest.fixture(scope = "function")  #область видимости
def create_booking(api_client): # Фикстура для создания бронирования
    print(f"DEBUG: Endpoints = {Endpoints}")
    print(f"DEBUG: type(Endpoints) = {type(Endpoints)}")
    print(f"DEBUG: Endpoints.BOOKING_ENDPOINT = {Endpoints.BOOKING_ENDPOINT}")
    print(f"DEBUG: type(Endpoints.BOOKING_ENDPOINT) = {type(Endpoints.BOOKING_ENDPOINT)}")
    print(f"DEBUG: Full URL = {api_client.base_url}{Endpoints.BOOKING_ENDPOINT}")
    payload = {
        "firstname": "Sally",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    }
    response = api_client.session.post(f"{api_client.base_url}{Endpoints.BOOKING_ENDPOINT}",json=payload,timeout=Timeouts.TIMEOUT)
    if response.status_code >= 400:
        raise Exception(f"Ошибка создания бронирования: {response.status_code} - {response.text}")

    return response.json() # Только для успешного ответа парсим JSON