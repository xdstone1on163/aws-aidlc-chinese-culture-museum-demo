"""API endpoint tests."""
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.accounts.models import EmailVerificationToken
from .factories import UserFactory, AdminFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client):
    user = UserFactory(email='auth@test.com', password='testpass123')
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def admin_client(api_client):
    admin = AdminFactory(email='admin@test.com', password='adminpass123')
    api_client.force_authenticate(user=admin)
    return api_client, admin


class TestRegisterView:
    def test_register_success(self, api_client):
        resp = api_client.post(reverse('accounts:register'), {
            'email': 'new@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'nickname': 'newuser',
        })
        assert resp.status_code == 201
        assert resp.data['code'] == 201

    def test_register_duplicate_email(self, api_client):
        UserFactory(email='dup@test.com')
        resp = api_client.post(reverse('accounts:register'), {
            'email': 'dup@test.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
            'nickname': 'unique',
        })
        assert resp.status_code == 400

    def test_register_weak_password(self, api_client):
        resp = api_client.post(reverse('accounts:register'), {
            'email': 'weak@test.com',
            'password': 'abcdefgh',
            'confirm_password': 'abcdefgh',
            'nickname': 'weakuser',
        })
        assert resp.status_code == 400


class TestLoginView:
    def test_login_success(self, api_client):
        UserFactory(email='login@test.com', password='testpass123')
        resp = api_client.post(reverse('accounts:login'), {
            'email': 'login@test.com',
            'password': 'testpass123',
        })
        assert resp.status_code == 200
        assert 'access' in resp.data['data']

    def test_login_wrong_password(self, api_client):
        UserFactory(email='wrong@test.com', password='testpass123')
        resp = api_client.post(reverse('accounts:login'), {
            'email': 'wrong@test.com',
            'password': 'wrongpass',
        })
        assert resp.status_code == 401


class TestVerifyEmail:
    def test_verify_success(self, api_client):
        from apps.accounts import services
        user = services.register_user('verify@test.com', 'testpass123', 'vuser')
        token = EmailVerificationToken.objects.get(user=user)
        resp = api_client.get(reverse('accounts:verify_email'), {'token': token.token})
        assert resp.status_code == 200


class TestMeView:
    def test_get_me(self, auth_client):
        client, user = auth_client
        resp = client.get(reverse('accounts:me'))
        assert resp.status_code == 200
        assert resp.data['data']['email'] == 'auth@test.com'

    def test_unauthenticated(self, api_client):
        resp = api_client.get(reverse('accounts:me'))
        assert resp.status_code == 401


class TestAdminViews:
    def test_user_list(self, admin_client):
        client, _ = admin_client
        UserFactory.create_batch(3)
        resp = client.get(reverse('accounts:user_list'))
        assert resp.status_code == 200

    def test_user_list_forbidden(self, auth_client):
        client, _ = auth_client
        resp = client.get(reverse('accounts:user_list'))
        assert resp.status_code == 403

    def test_toggle_active(self, admin_client):
        client, _ = admin_client
        user = UserFactory()
        resp = client.patch(
            reverse('accounts:toggle_user_active', args=[user.id]),
            {'is_active': False},
        )
        assert resp.status_code == 200

    def test_change_role(self, admin_client):
        client, _ = admin_client
        user = UserFactory()
        resp = client.patch(
            reverse('accounts:change_role', args=[user.id]),
            {'role': 'content_manager'},
        )
        assert resp.status_code == 200
