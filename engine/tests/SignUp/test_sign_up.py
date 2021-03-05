import pytest

@pytest.mark.django_db
def test_signup(client):
    response = client.post('/accounts/signup/', {
        'username': 'testuser',
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@django-test.com',
        'password': 'JaneDoe123!'
        })
    assert response.status_code == 302
