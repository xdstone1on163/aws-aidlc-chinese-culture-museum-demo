from django.apps import AppConfig


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.search'
    verbose_name = '搜索'

    def ready(self):
        import apps.search.signal_handlers  # noqa: F401
