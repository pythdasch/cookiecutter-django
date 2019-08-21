from django.urls import path

from {{ cookiecutter.project_slug }}.{{ cookiecutter.app_name }}.views import (
    {{ cookiecutter.app_name }}_update_view,
    {{ cookiecutter.app_name }}_detail_view,
)

app_name = "{{ cookiecutter.app_name }}"

urlpatterns = [
    path("~update/", view={{ cookiecutter.app_name }}_update_view, name="update"),
    path("<int:id>/", view={{ cookiecutter.app_name }}_detail_view, name="detail"),
]
