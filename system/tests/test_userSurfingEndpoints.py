from django.urls import reverse
from django.contrib.auth.models import User, AbstractUser
from rest_framework import status
from rest_framework.test import APIClient, APISimpleTestCase
from core.models import User
import pytest


@pytest.mark.django_db
class TestUserLinks:
    def test_if_user_is_anonymous_returns_302_redirected(self):
        # Arrange

        # Act
        client = APIClient()
        response = client.get('/marketplace/')

        # Assert
        assert response.status_code == status.HTTP_302_FOUND

    def test_for_any_user_about_returns_ok(self):
        client = APIClient()
        response = client.get('/about/')
        print(response.status_code)
        assert response.status_code == status.HTTP_200_OK

    def test_redirects_to_login_from_dashboard_without_registered_client(self):
        client = APIClient()
        response = client.get('/dashboard/')
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == (reverse('core:login') + '?next=' + reverse('system:dashboard'))

    def test_seeing_dashboard_after_login(self):
        client = APIClient()
        user = User.objects.create_user(username='pytest_user', password='pytest_password_1234')
        client.force_login(user)
        response = client.get('/dashboard/')
        assert response.status_code == status.HTTP_200_OK

    def test_my_bids(self):
        client = APIClient()
        user = User.objects.create_user(username='pytest_user', password='pytest_password_1234')
        client.force_login(user)
        response = client.get('/my-bids/')
        assert response.status_code == status.HTTP_200_OK

    def test_confirm_bids_are_redirecting(self):
        client = APIClient()
        user = User.objects.create_user(username='pytest_user', password='pytest_password_1234')
        client.force_login(user)
        client.force_login(user=user)
        response = client.get('/confirm-bids/')
        assert response.url == reverse('system:bid-summary')

