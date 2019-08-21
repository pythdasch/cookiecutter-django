from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _



class {{ cookiecutter.model_name }}DetailView(LoginRequiredMixin, DetailView):

    model = {{ cookiecutter.model_name }}
    slug_field = "slug"
    slug_url_kwarg = "slug"


user_detail_view = {{ cookiecutter.model_name }}DetailView.as_view()


class {{ cookiecutter.model_name }}UpdateView(LoginRequiredMixin, UpdateView):

    model = {{ cookiecutter.model_name }}
    fields = ["title", "content"]

    def get_success_url(self):
        return reverse("{{ cookiecutter.app_name }}:detail", kwargs={"slug": self.object.pk})

    def get_object(self):
        return {{ cookiecutter.model_name }}.objects.get(slug=self.object.slug)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


{{ cookiecutter.app_name }}_update_view = {{ cookiecutter.model_name }}UpdateView.as_view()
