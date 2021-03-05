import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_access_control(client, test_user):
    response = client.get('/accounts/private/')
    assert response.status_code == 200