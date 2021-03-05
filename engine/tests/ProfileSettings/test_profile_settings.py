import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_access_control(client, test_user):
    response = client.get('/accounts/profile/settings/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_update(client, test_user):
    assert test_user.first_name == "John"
    assert test_user.last_name == "Doe"
    assert test_user.email == "john.doe@django-test.com"
    new_first_name = "Henry"
    new_last_name = "Johnson"
    new_email = "henry.johnson@mypytest.com"
    response = client.post('/accounts/profile/settings/', {
        'first_name': new_first_name,
        'last_name': new_last_name,
        'email': new_email
    })
    validation = User.objects.get(pk=test_user.id)
    assert validation.first_name == new_first_name
    assert validation.last_name == new_last_name
    assert validation.email == new_email