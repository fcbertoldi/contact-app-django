import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


def test_list_contacts(client):
    response = client.get(reverse("core:contact-index"))
    assert response.status_code == 200
