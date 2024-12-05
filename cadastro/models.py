from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Person(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)

    def __str__(self):
        return self.get_full_name() or self.username

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")
