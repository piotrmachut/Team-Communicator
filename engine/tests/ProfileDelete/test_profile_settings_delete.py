import pytest
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_access_control(client, test_user):
    response = client.get('/accounts/profile/settings/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_delete(client, test_user):
    users_before_delete = User.objects.all().count()
    response = client.post('/accounts/profile/settings/delete/')
    users_after_delete = User.objects.all().count()
    assert users_after_delete == users_before_delete - 1
