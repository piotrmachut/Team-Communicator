import pytest
from django.contrib.auth.models import User
from engine.models import PrivateMessage

@pytest.mark.django_db
def test_private(client, test_user, second_test_user):
    response = client.get(f'/accounts/private/{second_test_user.id}/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_team_settings_add_user(client, test_user, second_test_user):
    sides_of_conversation = [test_user, second_test_user]
    pm_before = PrivateMessage.objects.filter(receiver_id__in=sides_of_conversation).filter(sender_id__in=sides_of_conversation).count()
    response = client.post(f'/accounts/private/{second_test_user.id}/', {
        'message_field': "Test message",
        })
    pm_after = PrivateMessage.objects.filter(receiver_id__in=sides_of_conversation).filter(sender_id__in=sides_of_conversation).count()
    assert pm_after == pm_before + 1
