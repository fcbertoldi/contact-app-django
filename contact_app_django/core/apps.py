from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contact_app_django.core"

    def ready(self) -> None:
        from . import signals  # noqa: F401
