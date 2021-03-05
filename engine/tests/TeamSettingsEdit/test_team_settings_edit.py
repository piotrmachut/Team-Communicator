import pytest
from django.contrib.auth.models import User
from engine.models import Team

@pytest.mark.django_db
def test_team_settings(client, test_user, test_team):
    response = client.get(f'/accounts/team/settings/edit/{test_team.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_settings_edit(client, test_user, test_team):
    assert test_team.name == "Testers"
    assert test_team.description == "Team for testing purposes"
    new_name = "Wrestlers"
    new_description = "Professional wrestling team"
    response = client.post(f'/accounts/team/settings/edit/{test_team.id}/', {
        'team_name': new_name,
        'team_description': new_description
        })
    validation = Team.objects.get(pk=test_team.id)
    assert validation.name == new_name
    assert validation.description == new_description
