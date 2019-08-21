from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from {{ cookiecutter.project_slug }}.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class {{ cookiecutter.name_of_model }}Admin(admin.ModelAdmin):
    pass
