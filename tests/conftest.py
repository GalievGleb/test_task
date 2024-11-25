"""Файл для фикстур pytest"""

from pytest import fixture
from requests import post, delete
BASE_URL = "https://restful-booker.herokuapp.com"


@fixture(scope="session")
def base_url():
    """Фикстура для базового URL."""
    return BASE_URL


@fixture(scope="function")
def create_booking():
    """Фикстура для создания бронирования."""
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-10-10",
            "checkout": "2023-10-15"
        },
        "additionalneeds": "Breakfast"
    }
    response = post(f"{BASE_URL}/booking", json=payload)
    response.raise_for_status()
    booking_id = response.json()["bookingid"]
    yield booking_id  # Передаем ID бронирования в тесты
    # Удаляем бронирование после тестов
    delete(f"{BASE_URL}/booking/{booking_id}", headers={"Cookie": "token=abc123"})
