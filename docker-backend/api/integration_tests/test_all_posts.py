import requests
import pytest


def test_get_all_posts():
    response = requests.get(
        "http://127.0.0.1:8000/api/posts/",
    )
    data = response.json()
    assert data.get("count") == 2


def test_get_all_posts_from_created_author():
    response = requests.get(
        "http://127.0.0.1:8000/api/posts/?author=Taro",
    )
    data = response.json()
    content = data.get('results')
    print(content)
    for post in content:
        if post.get('author_username') != 'Taro':
            pytest.fail('There is post of other author than Taro')


def test_get_posts_from_unexisting_author():
    response = requests.get(
        "http://127.0.0.1:8000/api/posts/?author=Tfsadfasa",
    )
    data = response.json()
    count = data.get("count")
    assert count == 0
