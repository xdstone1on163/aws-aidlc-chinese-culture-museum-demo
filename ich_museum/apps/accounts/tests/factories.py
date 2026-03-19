"""Test data factories."""
import factory
from apps.accounts.models import User, UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    role = 'user'
    is_active = True
    is_verified = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password(extracted or 'testpass123')
        if create:
            self.save()

    @factory.post_generation
    def profile(self, create, extracted, **kwargs):
        if create:
            UserProfileFactory(user=self)


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = factory.SubFactory(UserFactory, profile=None)
    nickname = factory.Sequence(lambda n: f'user{n}')
    language = 'zh'


class AdminFactory(UserFactory):
    role = 'admin'
    is_staff = True
    is_superuser = True


class ContentManagerFactory(UserFactory):
    role = 'content_manager'
