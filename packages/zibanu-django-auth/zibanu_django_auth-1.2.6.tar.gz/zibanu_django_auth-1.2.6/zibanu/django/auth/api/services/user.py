# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2024. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2024. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         16/04/23 18:17
# Project:      Zibanu - Django
# Module Name:  user
# Description:
# ****************************************************************
import logging
import traceback
import smtplib
import uuid

from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError as CoreValidationError
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from zibanu.django.auth.api import serializers
from zibanu.django.auth.lib.signals import on_change_password, on_request_password
from zibanu.django.auth.lib.signals import on_user_created, on_user_updated, on_user_deleted
from zibanu.django.auth.lib.utils import get_user
from zibanu.django.auth.models import User
from zibanu.django.lib import CodeGenerator
from zibanu.django.lib.utils import Email
from zibanu.django.lib.utils import ErrorMessages
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.exceptions import ValidationError
from zibanu.django.rest_framework.decorators import permission_required
from zibanu.django.rest_framework.viewsets import ModelViewSet


class UserService(ModelViewSet):
    """
    Set of REST Services for django User model
    """
    model = User
    serializer_class = serializers.UserListSerializer
    request_password_template = settings.ZB_AUTH_REQUEST_PASSWORD_TEMPLATE
    change_password_template = settings.ZB_AUTH_CHANGE_PASSWORD_TEMPLATE
    new_user_template = settings.ZB_AUTH_NEW_USER_TEMPLATE
    extended_serializer_class = serializers.UserExtendedSerializer
    roles_key = settings.ZB_AUTH_ROLES_KEY
    permissions_key = settings.ZB_AUTH_PERMISSIONS_KEY

    def _send_mail(self, subject: str, to: list, template: str, context: dict) -> None:
        """
        Protected method to send mail

        Parameters
        ----------
        subject: str
            Subject for email
        to: list[str...]
            List of email targets
        template: str
            Name of the email body template
        context: dic[str, Any]
            Context data required for email template

        Returns
        -------
        None
        """
        try:
            # TODO: Reformat to use class directly
            email = Email(subject=subject, to=to, context=context)
            email.set_text_template(template=template)
            email.set_html_template(template=template)
            email.send()
        except smtplib.SMTPException:
            pass

    def get_permissions(self):
        """
        Override method to get permissions for allow on_request_password action.

        Returns
        -------
        response: Response object with HTTP status (200 if success) and list of permissions dataset.
        """
        if self.action == "request_password":
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes.copy()
        return [permission() for permission in permission_classes]

    @method_decorator(permission_required("auth.view_user"))
    def list(self, request, *args, **kwargs) -> Response:
        """
        REST service to get list of users. Add a filter to get only active users.

        Parameters
        ----------
        request: rest_framework.request.Request
            HTTP request object
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict[str, Any]
            Keyword qualified arguments received by the method

        Returns
        -------
        response: Response
            Object response with HTTP status (200 if success) and list of users dataset.
        """
        user = get_user(request=request)
        if hasattr(user, "level"):
            level = user.level
        # TODO: Accept order_by in request.
        kwargs = dict({"order_by": "first_name", "is_active__exact": True})
        response = super()._list(request, *args, **kwargs)
        # Filter data by level
        if len(response.data) > 0:
            data = [x for x in response.data if x["level"] >= user.level]
        else:
            data = response.data
        return Response(data=data, status=response.status_code)

    @method_decorator(permission_required("auth.view_user"))
    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Method to get one user object from request filters.

        Parameters
        ----------
        request : rest_framework.request.Request
            HTTP request object
        args : tuple
            Arguments received by the method without keywords
        kwargs : dict[str, Any]
            Keyword qualified arguments received by the method

        Returns
        -------
        Response
        """
        self.serializer_class = serializers.UserSerializer
        response = super()._retrieve(request, *args, **kwargs)
        # Drop password field from data
        response.data.pop("password", None)
        return response

    def _create_user(self, request) -> User:
        """
        Create a new user from request data and return user object created

        Parameters
        ----------
        request : rest_framework.request.Request
            HTTP request object

        Returns
        -------
        User:
            User object created if success
        """
        try:
            user = get_user(request.user)
            roles_data = request.data.pop(self.roles_key, [])
            permissions_data = request.data.pop(self.permissions_key, [])
            # Set default values and automatic options
            if settings.ZB_AUTH_AUTO_PASSWORD:
                code_generator = CodeGenerator("create_user", is_safe=True,
                                               code_length=settings.ZB_AUTH_DEFAULT_PASSWORD_MIN_LENGTH)
                request.data["password"] = code_generator.get_alpha_numeric_code()
            if settings.ZB_AUTH_AUTO_USERNAME:
                request.data["username"] = uuid.uuid4().hex
            if "profile" not in request.data:
                request.data["profile"] = {}
            # Create an atomic transaction
            with transaction.atomic():
                serializer = self.extended_serializer_class(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    created_user = serializer.create(validated_data=serializer.validated_data)
                    if created_user is not None:
                        if len(roles_data) > 0:
                            # If user has groups to add
                            created_user.groups.set(roles_data)
                        if len(permissions_data) > 0:
                            # If user has permissions to add
                            created_user.user_permissions.set(permissions_data)
                        if user.level > created_user.level:
                            raise ValidationError(
                                _("The created user level cannot be higher than that of authenticated user."))
                    else:
                        raise ValidationError(_("Error creating user"))
        except ValidationError:
            raise
        except Exception:
            raise
        else:
            return created_user

    @method_decorator(permission_required(["auth.add_user", "zb_auth.add_userprofile"]))
    def create(self, request, *args, **kwargs) -> Response:
        """
        REST service to create user with its profile.

        Parameters
        ----------
        request: rest_framework.request.Request
            HTTP request object
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict
            Keyword qualified arguments received by the method

        Returns
        -------
        response: Response
            HTTP response object with status (200 if success).
        """
        try:
            if request.data is not None and len(request.data) > 0:
                created_user = self._create_user(request)
                data_return = self.get_serializer(created_user).data
                on_user_created.send(sender=self, user=data_return, request=request)
                context = {
                    "user": created_user,
                    "new_password": request.data.get("password")
                }
                self._send_mail(subject=_("New User"), to=[created_user.email],
                                template=self.new_user_template, context=context)
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
        except ValidationError as exc:
            raise APIException(detail=exc.detail, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except CoreValidationError as exc:
            raise APIException(detail=exc.message_dict, code=exc.code,
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(detail=str(exc)) from exc
        else:
            return Response(status=status.HTTP_201_CREATED, data=data_return)

    def _update_user(self, request) -> User:
        """
        Update one record of the user entity

        Parameters
        ----------
        request : rest_framework.request.Request
            HTTP request object received

        Returns
        -------
        User:
            User object updated with the request
        """
        user_request = get_user(request.user)
        user = user_request
        try:
            if "email" in request.data or "id" in request.data:
                # Add profile key if it does not exist
                if "profile" not in request.data:
                    request.data["profile"] = dict()
                # Remove password key
                request.data.pop("password", None)
                groups_data = request.data.pop(self.roles_key, None)
                permissions_data = request.data.pop(self.permissions_key, None)
                with transaction.atomic():
                    if user.id != request.data.get("id", None) or user.email != request.data.get(
                            "email", None):
                        # If authenticated user is different from user to change.
                        if "id" in request.data:
                            user = self.model.objects.get(pk=request.data.pop("id"))
                        else:
                            user = self.model.objects.get(email__exact=request.data.pop("email"))
                    # Save user groups and permissions
                    if groups_data is not None:
                        user.groups.set(groups_data)
                    if permissions_data is not None:
                        user.user_permissions.set(permissions_data)
                    # Save user data
                    serializer = serializers.UserExtendedSerializer(instance=user, data=request.data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        user_return = serializer.update(serializer.instance, serializer.validated_data)
                    if user_request.level > user_return.level:
                        raise ValidationError(_("You cannot upgrade a user with a higher level."))
            else:
                raise ValidationError(_("'email' or 'id' not found in request data"))
        except self.model.DoesNotExist:
            raise ValidationError(_("User does not exist."))
        except Exception:
            raise
        else:
            return user_return

    @method_decorator(permission_required(["auth.change_user", "zb_auth.change_userprofile"]))
    def update(self, request, *args, **kwargs) -> Response:
        """
        REST service to update user, including profile, groups and permissions.

        Parameters
        ----------
        request: rest_framework.request.Request
            object from HTTP
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict
            Keyword qualified arguments received by the method

        Returns
        -------
        response: Response object with HTTP status (200 if success).
        """
        try:
            user = self._update_user(request)
            serializer = serializers.UserExtendedSerializer(instance=user)
            user_data = serializer.data
            on_user_updated.send(sender=self, user=user_data, request=request)
        except ValidationError as exc:
            raise APIException(detail=exc.detail, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except ObjectDoesNotExist as exc:
            raise APIException(ErrorMessages.NOT_FOUND, http_status=status.HTTP_404_NOT_FOUND) from exc
        except Exception as exc:
            raise APIException(detail=str(exc), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK, data=user_data)

    @method_decorator(permission_required(["auth.delete_user", "zb_auth.delete_userprofile"]))
    def destroy(self, request, *args, **kwargs) -> Response:
        """
        REST service to delete one user object.

        Parameters
        ----------
        request: Request object from HTTP
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict
            Keyword qualified arguments received by the method

        Returns
        -------
        response: Response object with HTTP status (200 if success).
        """
        try:
            if "id" in request.data or "email" in request.data:
                request_user = get_user(request.user)
                if "id" in request.data:
                    user = self.model.objects.get(pk=request.data.get("id"))
                else:
                    user = self.model.objects.filter(email__exact=request.data.get("email")).first()
                if (user.is_staff or user.is_superuser) and not (request_user.is_staff or request_user.is_superuser):
                    raise ValidationError(_("Only staff or superuser can delete another superuser or staff."),
                                          "delete_user")
                elif user.email == request_user.email:
                    raise ValidationError(_("Cannot delete yourself."), "delete_user")
                else:
                    deleted_user = self.get_serializer(user).data
                    user.delete()
                    on_user_deleted.send(sender=self, user=deleted_user, request=request)
            else:
                logging.error("'id' not found in request data")
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "delete_user")
        except ObjectDoesNotExist as exc:
            logging.warning(str(exc))
            raise APIException(detail=ErrorMessages.NOT_FOUND, http_status=status.HTTP_404_NOT_FOUND) from exc
        except ProtectedError as exc:
            logging.warning(str(exc))
            raise APIException(detail=_("User has protected child records. Cannot delete."), code="delete_user",
                               http_status=status.HTTP_403_FORBIDDEN) from exc
        except ValidationError as exc:
            logging.warning(str(exc))
            raise APIException(detail=exc.detail, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            logging.critical(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        else:
            return Response(status=status.HTTP_200_OK)

    def get_avatar(self, request, *args, **kwargs):
        """
        Retrieve the avatar from user profile data

        Parameters
        ----------
        request : rest_framework.request.Request: Request object from HTTP
        *args : tuple
            Arguments received by the method without keywords
        kwargs : dict
            Keyword qualified arguments received by the method.

        Returns
        -------
        Original representation of field.
        """
        try:
            self.serializer_class = serializers.ProfileExtendedSerializer
            user = get_user(request.user)
            data_return = None
            status_return = status.HTTP_200_OK
            if hasattr(user, "profile"):
                serializer = self.get_serializer(instance=user.profile)
                data_return = serializer.data.get("avatar", None)
                if not data_return:
                    status_return = status.HTTP_204_NO_CONTENT
        except Exception as exc:
            logging.critical(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        else:
            return Response(data=data_return, status=status_return)

    def get_profile(self, request, *args, **kwargs) -> Response:
        """
        Method to get a user profile

        Parameters
        ----------
        request : rest_framework.request.Request
            HTTP request object
        args : tuple
            Arguments received by the method without keywords
        kwargs : dict
            Keyword qualified arguments received by the method

        Returns
        -------
        Response:
            HTTP response object

        """
        try:
            self.serializer_class = serializers.UserProfileSerializer
            user = get_user(request.user)
            data_return = None
            status_return = status.HTTP_200_OK
            if hasattr(user, "profile"):
                serializer = self.get_serializer(instance=user)
                data_return = serializer.data
                if not data_return:
                    status_return = status.HTTP_204_NO_CONTENT
        except Exception as exc:
            logging.critical(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        else:
            return Response(data=data_return, status=status_return)

    def change_password(self, request, *args, **kwargs) -> Response:
        """
        REST service to change the user's password.

        Parameters
        ----------
        request: rest_framework.request.Request
            HTTP request object
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict
            Keyword qualified arguments received by the method

        Returns
        -------
        response: Response
            HTTP response object with status (200 if success) and data
        """
        try:
            user = get_user(request.user)
            if request.data.get("old_password", None) is not None and request.data.get("new_password",
                                                                                       None) is not None:
                if request.data.get("old_password") == request.data.get("new_password"):
                    raise ValidationError({_("Change password"): _("The old and new password must be different")})
                if user.check_password(request.data.get("old_password")):
                    if user.profile.secure_password:
                        min_length = settings.ZB_AUTH_SECURE_PASSWORD_MIN_LENGTH
                        max_length = settings.ZB_AUTH_SECURE_PASSWORD_MAX_LENGTH
                        if not CodeGenerator.validate_code(code=request.data.get("new_password"),
                                                           min_length=min_length, max_length=max_length,
                                                           secure=True):
                            raise ValidationError({_("Change password"): _(
                                "The password must meet the following criteria: It must be between %(min_length)d and "
                                "%(max_length)d characters, at least one uppercase letter (A-Z), at least one "
                                "lowercase letter (a-z), at least one number (0-9), at least one special character "
                                "from the following: !#$%(percentage)s&()*+.-@/_ and must not contain blank spaces or "
                                "the letter (ñ or Ñ).") % {"min_length": min_length, "max_length": max_length,
                                                           "percentage": "%"}})
                    else:
                        min_length = settings.ZB_AUTH_DEFAULT_PASSWORD_MIN_LENGTH
                        max_length = settings.ZB_AUTH_DEFAULT_PASSWORD_MAX_LENGTH
                        if not CodeGenerator.validate_code(code=request.data.get("new_password"),
                                                           min_length=min_length, max_length=max_length):
                            raise ValidationError({_("Change password"): _(
                                "The password must meet the following criteria: It must be between %(min_length)d and "
                                "%(max_length)d characters long, may contain letters (a-z, A-Z), special characters "
                                "!#$%(percentage)s&()*+.-@/_ and digits (0-9). It must not contain blank spaces or the "
                                "letter (ñ or Ñ).") % {"min_length": min_length, "max_length": max_length,
                                                       "percentage": "%"}})

                    user.set_password(request.data.get("new_password"))
                    user.save()
                    context = {
                        "user": user
                    }
                    if apps.is_installed("zibanu.django"):
                        self._send_mail(subject=_("Password change"), to=[user.email],
                                        template=self.change_password_template, context=context)
                    on_change_password.send(sender=self.__class__, user=user, request=request)
                else:
                    raise ValidationError(_("Old password does not match."))
            else:
                logging.error("'old_password'/'new_password' not found in request")
                raise ValidationError({_("Change password"): _("Old/New password are required.")})
        except ValidationError as exc:
            logging.warning(str(exc))
            raise APIException(detail=exc.detail, http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            logging.critical(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        else:
            return Response(status=status.HTTP_200_OK)

    def request_password(self, request, *args, **kwargs) -> Response:
        """
        REST service to request password and send through email.

        Parameters
        ----------
        request: rest_framework.request.Request
            object from HTTP
        *args: tuple
            Arguments received by the method without keywords
        **kwargs: dict
            Keyword qualified arguments received by the method.

        Returns
        -------
        response: Response
            HTTP response object with status (200 if success) and data if exists.
        """
        try:
            if "email" in request.data:
                user = User.objects.filter(email__exact=request.data.get("email"), is_active__exact=True).first()
                if hasattr(user, "profile"):
                    secure_password = user.profile.secure_password
                else:
                    secure_password = False

                if user is not None:
                    code_gen = CodeGenerator(action="on_request_password")
                    if secure_password:
                        new_password = code_gen.get_secure_code(length=settings.ZB_AUTH_SECURE_PASSWORD_MIN_LENGTH)
                    else:
                        new_password = code_gen.get_alpha_numeric_code(
                            length=settings.ZB_AUTH_DEFAULT_PASSWORD_MIN_LENGTH)
                    user.set_password(new_password)
                    user.save()
                    context = {
                        "user": user,
                        "new_password": new_password
                    }
                    if apps.is_installed("zibanu.django"):
                        self._send_mail(subject=_("Request password."), to=[user.email],
                                        template=self.request_password_template, context=context)
                    on_request_password.send(sender=self.__class__, user=user, request=request)
                else:
                    raise ValidationError(_("Email is not registered or user is not active."))
            else:
                logging.error("'email' not found in request data")
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
        except ValidationError as exc:
            logging.warning(str(exc))
            raise APIException(detail=exc.detail[0], http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            logging.critical(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        else:
            return Response(status=status.HTTP_200_OK)
