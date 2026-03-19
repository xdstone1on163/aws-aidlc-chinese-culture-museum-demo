"""Model tests."""
import pytest
from apps.accounts.models import User, UserProfile, EmailVerificationToken, PasswordResetToken
from .factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(email='test@example.com', password='testpass123')
        assert user.email == 'test@example.com'
        assert user.role == 'user'
        assert user.is_active is True
        assert user.is_verified is False
        assert user.check_password('testpass123')

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@example.com', password='adminpass123')
        assert user.role == 'admin'
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.is_verified is True

    def test_email_required(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email='', password='testpass123')

    def test_str(self):
        user = UserFactory(email='hello@test.com')
        assert str(user) == 'hello@test.com'


class TestUserProfile:
    def test_auto_created_with_factory(self):
        user = UserFactory()
        assert hasattr(user, 'profile')
        assert user.profile.nickname is not None

    def test_str(self):
        user = UserFactory()
        assert str(user.profile) == user.profile.nickname


class TestTokenModels:
    def test_email_verification_token(self):
        user = UserFactory()
        token = EmailVerificationToken.objects.create(user=user)
        assert token.token is not None
        assert token.is_used is False
        assert token.is_expired is False

    def test_password_reset_token(self):
        user = UserFactory()
        token = PasswordResetToken.objects.create(user=user)
        assert token.token is not None
        assert token.is_used is False
        assert token.is_expired is False
