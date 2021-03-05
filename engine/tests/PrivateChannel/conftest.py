import pytest
from django.test import Client
from django.contrib.auth.models import User

@pytest.fixture
def test_user():
    test_user = User.objects.create_user(
        username="testuser",
        first_name="John",
        last_name="Doe",
        email="john.doe@django-test.com",
        password="JaneDoe123!"
    )
    return test_user

@pytest.fixture
def second_test_user():
    second_test_user = User.objects.create_user(
        username="testuser2",
        first_name="Sam",
        last_name="Winchester",
        email="sam.winchester@supernatural.com",
        password="Bobby123!"
    )
    return second_test_user

@pytest.fixture
def client(test_user, second_test_user):
    c = Client()
    c.login(username='testuser', password='JaneDoe123!')
    return c
