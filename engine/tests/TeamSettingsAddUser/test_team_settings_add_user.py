import pytest
from django.contrib.auth.models import User
from engine.models import Team

@pytest.mark.django_db
def test_team_settings(client, test_user, test_team, second_test_user):
    response = client.get(f'/accounts/team/settings/add-user/{test_team.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_settings_add_user(client, test_user, test_team, second_test_user):
    users_before = Team.objects.get(pk=test_team.id).users.all().count()
    response = client.post(f'/accounts/team/settings/add-user/{test_team.id}/', {
        'add-user': second_test_user.id,
        })
    users_after = Team.objects.get(pk=test_team.id).users.all().count()
    assert users_after == users_before + 1
