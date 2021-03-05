import pytest
from django.test import Client
from django.contrib.auth.models import User
from engine.models import Team

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
def test_team(test_user):
    team_owner = test_user.id
    test_team = Team.objects.create(
        name="Testers",
        description="Team for testing purposes",
        owner=User.objects.get(pk=test_user.id)
    )
    test_team.users.add(test_user)
    return test_team


@pytest.fixture
def client(test_user):
    c = Client()
    c.login(username='testuser', password='JaneDoe123!')
    return c
