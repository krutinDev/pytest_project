import pytest
import requests
import random

BASE_URL = "https://petstore.swagger.io/v2"

# Тестовые данные
test_pet = {
    "id": random.randint(1000, 9999),
    "category": {
        "id": 0,
        "name": "Dog"
    },
    "name": "Rex",
    "photoUrls": ["http://example.com/photo1.jpg"],
    "tags": [
        {
            "id": 0,
            "name": "friendly"
        }
    ],
    "status": "available"
}

updated_pet = {
    "id": test_pet["id"],
    "category": {
        "id": 0,
        "name": "Dog"
    },
    "name": "Max",
    "photoUrls": ["http://example.com/photo2.jpg"],
    "tags": [
        {
            "id": 0,
            "name": "friendly"
        }
    ],
    "status": "sold"
}

test_user = {
    "id": random.randint(1000, 9999),
    "username": f"user{random.randint(1000,9999)}",
    "firstName": "Test",
    "lastName": "User",
    "email": "testuser@example.com",
    "password": "password123",
    "phone": "123-456-7890",
    "userStatus": 1
}

@pytest.fixture(scope="module")  # Автоматически добавляет и удаляет питомца перед тестами
def add_pet():
    # Добавление питомца
    response = requests.post(f"{BASE_URL}/pet", json=test_pet)
    assert response.status_code == 200
    yield
    # Удаление питомца после теста
    requests.delete(f"{BASE_URL}/pet/{test_pet['id']}")


def test_add_pet(add_pet):
    assert add_pet is None  # Убедились в фикстуре


def test_get_pet_by_id():
    response = requests.get(f"{BASE_URL}/pet/{test_pet['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_pet["id"]
    assert data["name"] == test_pet["name"]
    assert data["status"] == test_pet["status"]


def test_update_pet():
    response = requests.put(f"{BASE_URL}/pet", json=updated_pet)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_pet["name"]
    assert data["status"] == updated_pet["status"]

    # Проверка обновления
    get_response = requests.get(f"{BASE_URL}/pet/{test_pet['id']}")
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["name"] == updated_pet["name"]
    assert get_data["status"] == updated_pet["status"]


def test_find_pets_by_status():
    status = "sold"
    response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": status})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Проверяем, что среди результатов есть наш обновлённый питомец
    pet_ids = [pet["id"] for pet in data]
    assert test_pet["id"] in pet_ids


def test_delete_pet():
    response = requests.delete(f"{BASE_URL}/pet/{test_pet['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == str(test_pet["id"])

    # Проверка удаления
    get_response = requests.get(f"{BASE_URL}/pet/{test_pet['id']}")
    assert get_response.status_code == 404


def test_create_user():
    response = requests.post(f"{BASE_URL}/user", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == str(test_user["id"])


def test_login_user():
    response = requests.get(f"{BASE_URL}/user/login", params={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    assert "logged in user session" in response.text.lower()


def test_delete_user():
    response = requests.delete(f"{BASE_URL}/user/{test_user['username']}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == test_user["username"]

    # Проверка удаления
    get_response = requests.get(f"{BASE_URL}/user/{test_user['username']}")
    assert get_response.status_code == 404