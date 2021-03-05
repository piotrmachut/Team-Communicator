import pytest
from django.contrib.auth.models import User
from engine.models import Team

@pytest.mark.django_db
def test_team_settings(client, test_user, test_team):
    response = client.get(f'/accounts/team/settings/delete/{test_team.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_settings_edit(client, test_user, test_team):
    teams_before_delete = Team.objects.all().count()
    response = client.post(f'/accounts/team/settings/delete/{test_team.id}/')
    teams_after_delete = Team.objects.all().count()
    assert teams_after_delete == teams_before_delete - 1
