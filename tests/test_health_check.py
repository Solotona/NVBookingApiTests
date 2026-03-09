import pytest
import allure
import faker
import requests

@allure.feature('Test Ping')
@allure.story('Test connection')
def test_ping(api_client):  # Тестовая функция с фикстурой api_client
    status_code = api_client.ping() # Обращаемся к фикстуре, которая возвращает объект класса вместе с методами
    assert status_code == 201, f"Expected status 201 but got {status_code}"


# Мокирование
@allure.feature('Test Ping')
@allure.story('Test server unavailability') # Проверка, что метод ping() корректно реагирует на недоступность сервера - тестирование обработки ошибок
def test_ping_server_unavailable(api_client, mocker): # обращаемся к фикстуре mocker, которая подменяем сетевой запрос на исключение
    mocker.patch.object( # Обращаемся к mocker пропатчить объект (сессия), подменить ответ на get запрос
        api_client.session,  # Объект, метод которого подменяем
        'get',
        side_effect=Exception("Server unavailable"))  # Что должно произойти при вызове
    with pytest.raises(Exception, match='Server unavailable'):  # Ожидаем, что ping() выбросит исключение с правильным текстом
        api_client.ping()  # Когда код внутри api_client.ping() вызовет self.session.get(...), вместо реального запроса сработает мок


@allure.feature('Test Ping')
@allure.story('Test wrong HTTP method')
def test_ping_wrong_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, 'get', return_value = mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 405"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test server error')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'get', return_value = mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 500"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test wrong URL')
def test_ping_internal_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, 'get', return_value = mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 404"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test connection with different success code')
def test_ping_success_different_method(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mocker.patch.object(api_client.session, 'get', return_value = mock_response)
    with pytest.raises(AssertionError, match="Expected status 201 but got 200"):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test timeout')
def test_ping_timeout(api_client, mocker):
    mocker.patch.object(api_client.session, 'get', side_effect = requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.ping()


@allure.feature('Test Ping')
@allure.story('Test delayed response')
def test_ping_delayed_response(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mocker.patch.object(api_client.session, 'get', return_value = mock_response)
    status_code = api_client.ping()

    assert status_code == 201, f"Expected status 201 but got {status_code}"