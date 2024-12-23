from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Person(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)
    password_email = models.CharField(max_length=255)
    profile_image = models.ImageField(
        _("profile image"), upload_to="profile_images/", blank=True, null=True
    )

    def get_full_name(self):
        return super().get_full_name() or self.username

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
