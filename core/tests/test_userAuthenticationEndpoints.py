from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APISimpleTestCase
import pytest


@pytest.mark.django_db
class TestCoreUrlLinks:
    def test_login(self):
        client = APIClient()
        response = client.post('/login/', {'username': 'tapati', 'password': 'soumya1234'})
        assert response.status_code == status.HTTP_200_OK

    def test_if_redirecting_after_logout(self):
        client = APIClient()
        response = client.post('/logout/')
        assert response.url == (reverse('core:login') + '?next=' + reverse('core:logout'))

    def test_if_user_can_register(self):
        client = APIClient()
        response = client.post(
            '/register/',
            json={
                'username': 'pytest_user',
                'password': 'pytest_password',
                'email': 'pytest@gmail.com',
                'first_name': 'pytest_first_name',
                'last_name': 'pytest_last_name',
                'phone': '123456789',
                'birth_date': '2001-07-27',
                'address': 'throughout india'
            }
        )
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_admin_it_is_redirecting(self):
        client = APIClient()
        client.force_authenticate(user=User())
        response = client.get('/admin/system/auction/')
        assert response.status_code == status.HTTP_302_FOUND