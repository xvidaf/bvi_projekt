from django.contrib.sites.models import Site
from django.db import models

from django.utils.translation import gettext_lazy as _


class HoneypotSetting(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE,)
    log_django_admin = models.BooleanField()
    log_previous_page = models.BooleanField()

class MovementLog(models.Model):
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    path = models.TextField(_("path"), blank=True, null=True)
    previous_page = models.TextField(_("previous page"), blank=True, null=True)

    class Meta:
        verbose_name = _("movement log")
        verbose_name_plural = _("movement logs")
        ordering = ('timestamp',)
