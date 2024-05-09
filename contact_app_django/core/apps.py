from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "contact_app_django.core"

    def ready(self) -> None:
        from contact_app_django.tasks import init as tasks_init

        from .services import archiver

        tasks_init(archiver=archiver)
