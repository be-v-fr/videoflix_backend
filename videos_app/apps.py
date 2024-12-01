from django.apps import AppConfig


class VideosAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos_app'

    def ready(self):
        from . import signals
        return super().ready()