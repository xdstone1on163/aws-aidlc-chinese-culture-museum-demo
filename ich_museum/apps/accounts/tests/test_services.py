"""Service layer tests."""
import pytest
from apps.accounts import services
from apps.accounts.models import User, EmailVerificationToken, PasswordResetToken
from .factories import UserFactory, AdminFactory

pytestmark = pytest.mark.django_db


class TestRegistration:
    def test_register_user(self):
        user = services.register_user('new@test.com', 'testpass123', 'newuser')
        assert user.email == 'new@test.com'
        assert user.is_verified is False
        assert hasattr(user, 'profile')
        assert user.profile.nickname == 'newuser'
        assert EmailVerificationToken.objects.filter(user=user).exists()

    def test_verify_email_success(self):
        user = services.register_user('v@test.com', 'testpass123', 'vuser')
        token = EmailVerificationToken.objects.get(user=user)
        ok, msg = services.verify_email(token.token)
        assert ok is True
        user.refresh_from_db()
        assert user.is_verified is True

    def test_verify_email_invalid_token(self):
        ok, msg = services.verify_email('invalid-token')
        assert ok is False
        assert '无效' in msg

    def test_verify_email_used_token(self):
        user = services.register_user('u@test.com', 'testpass123', 'uuser')
        token = EmailVerificationToken.objects.get(user=user)
        services.verify_email(token.token)
        ok, msg = services.verify_email(token.token)
        assert ok is False
        assert '已使用' in msg


class TestLogin:
    def test_login_success(self):
        UserFactory(email='login@test.com', password='testpass123')
        tokens, error = services.login_user('login@test.com', 'testpass123')
        assert error is None
        assert 'access' in tokens
        assert 'refresh' in tokens
        assert tokens['user']['email'] == 'login@test.com'

    def test_login_wrong_password(self):
        UserFactory(email='wrong@test.com', password='testpass123')
        tokens, error = services.login_user('wrong@test.com', 'wrongpass')
        assert tokens is None
        assert '邮箱或密码错误' in error

    def test_login_disabled_user(self):
        UserFactory(email='disabled@test.com', password='testpass123', is_active=False)
        tokens, error = services.login_user('disabled@test.com', 'testpass123')
        assert tokens is None
        assert '禁用' in error


class TestPasswordReset:
    def test_request_reset(self):
        user = UserFactory(email='reset@test.com')
        services.request_password_reset('reset@test.com')
        assert PasswordResetToken.objects.filter(user=user).exists()

    def test_reset_password_success(self):
        user = UserFactory(email='rp@test.com', password='oldpass123')
        services.request_password_reset('rp@test.com')
        token = PasswordResetToken.objects.get(user=user)
        ok, msg = services.reset_password(token.token, 'newpass123')
        assert ok is True
        user.refresh_from_db()
        assert user.check_password('newpass123')

    def test_reset_password_invalid_token(self):
        ok, msg = services.reset_password('bad-token', 'newpass123')
        assert ok is False


class TestUserManagement:
    def test_disable_user(self):
        user = UserFactory()
        services.disable_user(user.id)
        user.refresh_from_db()
        assert user.is_active is False

    def test_enable_user(self):
        user = UserFactory(is_active=False)
        services.enable_user(user.id)
        user.refresh_from_db()
        assert user.is_active is True

    def test_change_role(self):
        admin = AdminFactory()
        user = UserFactory()
        ok, msg = services.change_user_role(user.id, 'content_manager', admin)
        assert ok is True
        user.refresh_from_db()
        assert user.role == 'content_manager'

    def test_change_own_role_denied(self):
        admin = AdminFactory()
        ok, msg = services.change_user_role(admin.id, 'user', admin)
        assert ok is False
        assert '自己' in msg
