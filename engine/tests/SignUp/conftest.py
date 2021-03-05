import pytest
from django.test import Client

@pytest.fixture
def client():
    c = Client()
    return c
