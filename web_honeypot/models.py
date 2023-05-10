from django.contrib.sites.models import Site
from django.db import models

from django.utils.translation import gettext_lazy as _


class HoneypotSetting(models.Model):
    site = models.OneToOneField(Site, on_delete=models.CASCADE,)
    log_django_admin = models.BooleanField(default=False)
    log_previous_page = models.BooleanField(default=False)
    log_review_creation = models.BooleanField(default=False)
    log_restaurant_creation = models.BooleanField(default=False)
    allow_review_creation = models.BooleanField(default=False)
    allow_restaurant_creation = models.BooleanField(default=False)
    log_SQL = models.BooleanField(default=False)
class MovementLog(models.Model):
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    path = models.TextField(_("path"), blank=True, null=True)
    previous_page = models.TextField(_("previous page"), blank=True, null=True)

class ReviewLog(models.Model):
    restaurant = models.IntegerField(_("restaurant"), blank=True, null=True)
    name = models.CharField(_("name"), max_length=255, blank=True, null=True)
    rating = models.IntegerField(_("rating"), blank=True, null=True)
    comment = models.CharField(_("comment"), max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

class RestaurantLog(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True, null=True)
    street_address = models.CharField(_("street address"), max_length=255, blank=True, null=True)
    description = models.CharField(_("description"), max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("restaurant log")
        verbose_name_plural = _("restaurant logs")
        ordering = ('timestamp',)

class SqlLog(models.Model):
    action = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    SQL = models.CharField(_("session key"), max_length=500000, blank=True, null=True)
    ip_address = models.GenericIPAddressField(_("ip address"), protocol='both', blank=True, null=True)
    session_key = models.CharField(_("session key"), max_length=50, blank=True, null=True)
    user_agent = models.TextField(_("user-agent"), blank=True, null=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("sql log")
        verbose_name_plural = _("sql logs")
        ordering = ('timestamp',)