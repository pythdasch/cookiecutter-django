from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class {{ cookiecutter.model_name }}Config(AppConfig):
    name = "{{ cookiecutter.project_slug }}.{{ cookiecutter.app_name }}"
    verbose_name = _("{{ cookiecutter.app_name }}")

    def ready(self):
        try:
            import {{ cookiecutter.project_slug }}.{{ cookiecutter.app_name }}.signals  # noqa F401
        except ImportError:
            pass
