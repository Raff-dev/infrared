from rest_framework.test import APIClient

client = APIClient()


def test_index():
    res = client.get("/").json()
    assert res == {"Hello": "world!"}
