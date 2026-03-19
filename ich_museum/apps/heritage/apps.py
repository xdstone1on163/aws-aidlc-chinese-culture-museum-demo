from django.apps import AppConfig


class HeritageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.heritage'
    verbose_name = '非遗项目'

    def ready(self):
        import apps.heritage.signals  # noqa: F401
