from http.client import responses

import requests
import os # встроенный модуль для работы с файлами
from dotenv import load_dotenv # устанавливаем библиотеку python-dotenv. Функция load_dotenv проводит анализ файла .env, а затем загружает все найденные переменные в качестве переменных окружения""""
from requests.auth import HTTPBasicAuth

from core.settings.environments import Environment
from core.clients.endpoints import Endpoints
from core.settings.config import Users, Timeouts

import allure

load_dotenv()

# создаем класс APIClient — обёртку для работы с внешними сервисами через API
class APIClient:
    def __init__(self):
        # 1. Получаем значение переменной окружения ENVIROMENT. Из Current File - Edit Configurations.. - Edit configurations templates - Python Tests - Autodetect
        environment_str = os.getenv('ENVIRONMENT')

        # 2. Преобразуем строку в член перечисления Environment. Enviroment[environment_str] — пытается найти соответствующий член перечисления.
        try:
            environment = Environment[environment_str]
        # Если значение не совпадает ни с Environment.TEST, ни с Environment.PROD — выбрасывается KeyError
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}")

        # 3. Устанавливаем базовый URL в зависимости от среды
        self.base_url = self.get_base_url(environment)

        # 4. Сздаём объект сессии из библиотеки requests, который используется для выполнения HTTP-запросов: сессия сохраняет соединения между запросами, сессия автоматически сохраняет и отправляет куки между запросами
        self.session = requests.Session()

        # 4. Задаём стандартные заголовки по умолчанию для всех запросов (в данном случае — формат данных application/json).
        self.session.headers = {
        'Content-Type': 'application/json'
        }

    # Используем метод get_base_url для определения базового URL API в зависимости от окружения
    # Первый аргумент self говорит, что этот код будет работать с конкретным объектом класса
    # Метод примает параметр environment. Это перечисление (TEST или PROD).
    # Возвращает строку (str) - базовый адрес сервера в зависимости от окружения
    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f"Unsupported environment: {environment}")

    def get(self, endpoint, params=None, statusCode=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.session.headers, params=params)
        if statusCode:
            assert response.status_code == statusCode
        return response.json() # Метод response.json() в Python (обычно используемый в библиотеке requests) преобразует полученный от сервера ответ в формате JSON (строку) в удобные для работы структуры данных Python — словари (dict) или списки (list). Он автоматически декодирует JSON-контент, позволяя сразу обращаться к данным

    def post(self, endpoint, data=None, statusCode=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if statusCode:
            assert response.status_code == statusCode
        return response.json()

    # Создаем метод класса, который предназначен для проверки доступности («пинга») API.
    def ping(self):
        with allure.step('Ping api client'):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status() # Функция response.raise_for_status() в библиотеке requests нужна для автоматической проверки успешности HTTP-запроса. Если сервер вернул код ошибки (4xx или 5xx, например, 404 или 500), функция вызывает исключение requests.exceptions.HTTPError. Это предотвращает дальнейшую обработку ошибочных данных
        with allure.step('Assert status code'):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    # Создаем метод auth, который выполняет аутентификацию пользователя и сохраняет токен для последующих запросов
    def auth(self):
        with allure.step('Getting authenticate'):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}" # Формирует полный URL для запроса, объединяя базовый адрес (self.base_url) и путь к эндпоинту аутентификации (Endpoints.AUTH_ENDPOINT)
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD} # Создаёт тело запроса (payload) с учётными данными из класса Users
            response = self.session.post(url, json = payload, timeout = Timeouts.TIMEOUT) # Отправляет POST-запрос через сессию (self.session) с JSON-данными и заданным таймаутом
            response.raise_for_status()  # Функция response.raise_for_status() в библиотеке requests нужна для автоматической проверки успешности HTTP-запроса. Если сервер вернул код ошибки (4xx или 5xx, например, 404 или 500), функция вызывает исключение requests.exceptions.HTTPError. Это предотвращает дальнейшую обработку ошибочных данных
            with allure.step('Checking status code'):
                assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
            token = response.json().get("token") # Парсит JSON-ответ и извлекает значение поля "token"
            with allure.step('Updating header with authorization'):
                self.session.headers.update({"Authorization": f"Bearer {token}"}) # Добавляет заголовок авторизации в сессию, чтобы все последующие запросы автоматически включали токен

    def get_booking_by_id(self, booking_id):
        with allure.step('Getting object with bookings by ID'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.get(url, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        return response.json()

    def delete_booking(self, booking_id):
        with allure.step('Deleting booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.delete(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD))
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 201, f"Expected 200 but got {response.status_code}"
        return response.status_code == 201

    def create_booking(self, booking_data):
        with allure.step('Creating booking'):
            url = url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.post(url, json=booking_data)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        return response.json()

    def get_booking_ids(self, params=None):
        with allure.step('Getting object with bookings'):
            url = url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}"
            response = self.session.get(url, params=params)
            response.raise_for_status()
        with allure.step('Checking status code'):
            assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
        return response.json()

    def update_booking(self, booking_id, updated_booking_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.put(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD), json=updated_booking_data, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
            with allure.step('Checking status code'):
                assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
            return response.json()

    def partial_update_booking(self, booking_id, partial_updated_booking_data):
        with allure.step('Updating booking'):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            response = self.session.patch(url, auth=HTTPBasicAuth(Users.USERNAME, Users.PASSWORD), json=partial_updated_booking_data, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
            with allure.step('Checking status code'):
                assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
            return response.json()