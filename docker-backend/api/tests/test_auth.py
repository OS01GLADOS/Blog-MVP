import requests

# api login test

test_login_data_true = {"username": "Taro", "password": 1234}

test_login_data_false = {"username": "Taro", "password": 12}


def test_login_correct_credentials():
    response = requests.post(
        "http://127.0.0.1:8000/api/token/", json=(test_login_data_true)
    )
    assert response.status_code == 200


def test_login_incorrect_credentials():
    response = requests.post(
        "http://127.0.0.1:8000/api/token/", json=(test_login_data_false)
    )
    assert response.status_code == 401


# url = ..
