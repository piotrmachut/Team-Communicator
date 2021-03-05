import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_team_settings(client, test_user, test_team):
    response = client.get(f'/accounts/team/{test_team.id}/')
    assert response.status_code == 200
