# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         10/04/23 13:52
# Project:      Django Plugins
# Module Name:  models
# Description:
# ****************************************************************
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.translation import gettext_lazy as _
from timezone_utils.choices import ALL_TIMEZONES_CHOICES

from zibanu.django.db import models
from zibanu.django.lib import get_request_from_stack
from zibanu.django.lib import get_user
from zibanu.django.auth.lib.enums import GroupLevelEnum

# Constants
USER_BASE_CLASS = get_user_model()


class User(USER_BASE_CLASS):
    """
    Proxy class for user Model.
    """

    class Meta:
        """
        Metaclass for User proxy model
        """
        proxy = True

    @property
    def level(self):
        """
        Proxy property to get user level
        Returns
        -------
        int: User level. Default 5
        """
        if self.is_superuser:
            level = GroupLevelEnum.SUPER_USER
        elif self.is_staff:
            level = GroupLevelEnum.STAFF
        else:
            level = GroupLevelEnum.OPERATOR

            groups = self.groups.all()
            if groups is not None and groups.count() > 0:
                for group in groups:
                    try:
                        level = group.group_level.level if group.group_level.level < level else level
                    except ObjectDoesNotExist:
                        pass
        return level


class UserProfile(models.Model):
    """
    UserProfile model to store
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile",
                                related_query_name="user")
    timezone = models.CharField(max_length=50, null=False, blank=False, default="UTC",
                                choices=ALL_TIMEZONES_CHOICES, verbose_name=_("Time Zone"))
    theme = models.CharField(max_length=50, default=settings.ZB_AUTH_DEFAULT_THEME, null=False, blank=False,
                             verbose_name=_("User Theme"))
    lang = models.CharField(max_length=3, null=False, blank=False, default="en", verbose_name=_("Language"))
    avatar = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name=_("Avatar"))
    messages_timeout = models.IntegerField(default=10, null=False, blank=False, verbose_name=_("Message's Timeout"))
    keep_logged_in = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Keep Logged In"))
    multiple_login = models.BooleanField(default=False, null=False, blank=False, verbose_name=_("Allow multiple login"))
    secure_password = models.BooleanField(default=False, null=False, blank=False,
                                          verbose_name=_("Force secure password"))
    app_settings = models.JSONField(null=True, blank=True, verbose_name=_("Custom Application Profile"))

    class Meta:
        """
        Metaclass for UserProfile model
        """
        db_table = "zb_auth_user_profile"
        permissions = [
            ("change_userprofile_multiple_login", _("Can change multiple logged in user's profile"))
        ]

    def clean(self):
        """
        Override method to validate if ZB_AUTH_ALLOW_MULTIPLE_LOGIN setting is TRUE and if user has permission to change
        multiple_login flag
        """
        # Set validate multiple login flag
        validate_m_login_permissions = False

        # If not ZB_AUTH_ALLOW_MULTIPLE_LOGIN force false for common users.
        # otherwise, validate permissions.
        if not settings.ZB_AUTH_ALLOW_MULTIPLE_LOGIN:
            if not self.user.is_staff and not self.user.is_superuser:
                self.multiple_login = False

        if not self._state.adding:
            # Update record
            old_profile = UserProfile.objects.filter(user=self.user).first()
            if old_profile:
                # If old profile exists.
                if old_profile.avatar and self.avatar:
                    if old_profile.avatar.file.read() == self.avatar.file.read():
                        self.avatar = old_profile.avatar

                if old_profile.multiple_login != self.multiple_login:
                    validate_m_login_permissions = True
        else:
            if self.multiple_login:
                validate_m_login_permissions = True

        # If validate permissions is required.
        if validate_m_login_permissions:
            # Get Request object.
            request = get_request_from_stack()
            if request:
                auth_user = get_user(request.user)
                if not auth_user.is_staff and not auth_user.is_superuser and not auth_user.has_perm("zb_auth.change_userprofile_multiple_login"):
                    raise ValidationError(
                        {_("User Profile"): _("You are not allowed to change multiple logged in user's profile.")}
                    )


class GroupLevel(models.Model):
    """
    GroupLevel model to store the assigned level to each django permissions group
    """
    group = models.OneToOneField(Group, null=False, on_delete=models.CASCADE, verbose_name=_("Group"),
                                 help_text=_("Group to assign level"), related_name="group_level")
    level = models.IntegerField(default=GroupLevelEnum.OPERATOR, null=False, verbose_name=_("Group level"),
                                help_text=_("Level assigned to the group"))

    def __str__(self):
        """
        Cadena que retorna el texto a visualizar en las vistas de django

        Returns
        -------
        Group Name
        """
        return self.group.name

    class Meta:
        """
        Metaclass for GroupLevel model
        """
        db_table = "zb_auth_group_level"
