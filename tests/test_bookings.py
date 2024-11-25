from allure_commons._allure import step
from pytest import mark
from requests import post, delete, get, put
from typing import Dict, Any


@mark.parametrize("firstname,lastname,totalprice", [
    ("John", "Doe", 200),
    ("Alice", "Smith", 150)
])
def test_create_booking(base_url: str, firstname: str, lastname: str, totalprice: int) -> None:
    """
    Позитивный тест на создание бронирования.

    Args:
        base_url: Базовый URL для API.
        firstname: Имя клиента.
        lastname: Фамилия клиента.
        totalprice: Общая стоимость бронирования.
    """
    with step("Создаем бронирование"):
        payload: Dict[str, Any] = {
            "firstname": firstname,
            "lastname": lastname,
            "totalprice": totalprice,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-11-01",
                "checkout": "2023-11-05"
            },
            "additionalneeds": "Dinner"
        }
        response = post(f"{base_url}/booking", json=payload)
        assert response.status_code == 200, "Не удалось создать бронирование"
        booking_id: int = response.json()["bookingid"]

    with step("Проверяем данные бронирования"):
        response = get(f"{base_url}/booking/{booking_id}")
        assert response.status_code == 200, "Не удалось получить данные бронирования"
        data: Dict[str, Any] = response.json()
        assert data["firstname"] == firstname
        assert data["lastname"] == lastname
        assert data["totalprice"] == totalprice


def test_delete_non_existent_booking(base_url: str) -> None:
    """
    Негативный тест: удаление несуществующего бронирования.

    Args:
        base_url: Базовый URL для API.
    """
    with step("Пытаемся удалить несуществующее бронирование"):
        response = delete(f"{base_url}/booking/999999", headers={"Cookie": "token=abc123"})
        assert response.status_code == 403, "Удаление несуществующего бронирования должно возвращать 403"


def test_update_booking(create_booking: int, base_url: str) -> None:
    """
    Позитивный тест: обновление существующего бронирования.

    Args:
        create_booking: Идентификатор созданного бронирования.
        base_url: Базовый URL для API.
    """
    booking_id: int = create_booking
    with step("Обновляем бронирование"):
        payload: Dict[str, str] = {"firstname": "Updated", "lastname": "User"}
        response = put(
            f"{base_url}/booking/{booking_id}",
            json=payload,
            headers={"Cookie": "token=abc123"}
        )

        # Проверяем статус код и выводим тело ответа при ошибке
        assert response.status_code == 200, f"Не удалось обновить бронирование. Ответ: {response.text}"

    # Дополнительная проверка, чтобы увидеть данные, если тест не пройдет
    if response.status_code != 200:
        print("Ответ от API:", response.text)