from django.db import models
from django.conf import settings
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from stdimage.models import StdImageField
from core.models import Location
from ..utils.validators import validate_image


class {{ cookiecutter.name_of_model }}(Location):

    title = CharField(_("Name of User"), blank=True, max_length=255)
    title = models.CharField(verbose_name=_(
        "Title"), max_length=255, help_text=_("Title of your {{ cookiecutter.name_of_model }}"))
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name=_("Content"))

    # images
    image = StdImageField(
        verbose_name=_("Your logo"),
        upload_to='projects/cover/',
        blank=True, null=True,
        validators=[validate_image],
        variations=settings.IMAGE_CONFIG["VARIATIONS_IMAGES"])
    background = StdImageField(
        verbose_name=_("Background"),
        upload_to='projects/background/',
        blank=True, null=True,
        validators=[validate_image],
        variations=settings.IMAGE_CONFIG["VARIATIONS_IMAGES"])

    is_premium = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("annonces:detail", kwargs={"pk": self.pk})
