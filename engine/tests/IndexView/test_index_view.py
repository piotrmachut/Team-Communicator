import pytest

def test_indexview(client):
    response = client.get('')
    assert response.status_code == 200
