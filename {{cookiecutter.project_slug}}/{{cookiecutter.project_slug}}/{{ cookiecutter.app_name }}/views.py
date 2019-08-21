from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _



class {{ cookiecutter.name_of_model }}DetailView(LoginRequiredMixin, DetailView):

    model = {{ cookiecutter.name_of_model }}
    slug_field = "slug"
    slug_url_kwarg = "slug"


user_detail_view = {{ cookiecutter.name_of_model }}DetailView.as_view()


class {{ cookiecutter.name_of_model }}UpdateView(LoginRequiredMixin, UpdateView):

    model = {{ cookiecutter.name_of_model }}
    fields = ["title", "content"]

    def get_success_url(self):
        return reverse("{{ cookiecutter.app_name }}:detail", kwargs={"slug": self.object.pk})

    def get_object(self):
        return {{ cookiecutter.name_of_model }}.objects.get(slug=self.object.slug)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


{{ cookiecutter.app_name }}_update_view = {{ cookiecutter.name_of_model }}UpdateView.as_view()
