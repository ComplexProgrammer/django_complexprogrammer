from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"
    verbose_name = "Loyihalar"

    def ready(self):
        from projects import signals  # noqa: F401 — tests (kitob 49/50) -> AvtoTest sinxronlaş
