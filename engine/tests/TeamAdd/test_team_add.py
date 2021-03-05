import pytest
from django.contrib.auth.models import User
from engine.models import Team

@pytest.mark.django_db
def test_access_control(client, test_user):
    response = client.get('/accounts/team/add/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_add(client, test_user):
    teams_before = len(Team.objects.all())
    response = client.post('/accounts/team/add/', {
        'team_name': 'Testers',
        'team_description': "Team for testing purposes"
        })
    teams_after = len(Team.objects.all())
    assert teams_after == teams_before + 1
