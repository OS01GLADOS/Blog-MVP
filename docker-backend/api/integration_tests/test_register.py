import requests

user = {
    "username": "TestUser1",
    "password": 'password',
    'email': "testUser@gmail.com",
}


def register_user():
    response = requests.post(
        "http://127.0.0.1:8000/api/profiles/", json=(user)
    )
    assert response.status_code == 200

    response = requests.post(
        "http://127.0.0.1:8000/api/token/",
        json=(
            {
                "username": "TestUser1",
            }
        ),
    )
    assert response.status_code == 200
