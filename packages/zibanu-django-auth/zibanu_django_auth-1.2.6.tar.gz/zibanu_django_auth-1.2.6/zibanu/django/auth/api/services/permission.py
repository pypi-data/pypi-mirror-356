# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2024. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2024. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         19/06/23 11:00
# Project:      Zibanu - Django
# Module Name:  permission
# Description:
# ****************************************************************
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from zibanu.django.auth.api.serializers import PermissionSerializer
from zibanu.django.rest_framework.decorators import permission_required
from zibanu.django.rest_framework.viewsets import ModelViewSet


class PermissionService(ModelViewSet):
    """
    Set of REST Services for Permission model
    """
    model = Permission
    serializer_class = PermissionSerializer

    @method_decorator(permission_required(("is_staff", "auth.view_permission")))
    def list(self, request, *args, **kwargs) -> Response:
        """
        REST service for list permissions

        Parameters
        ----------
        request: Request object from HTTP
        *args: Tuple of parameters
        **kwargs: Dictionary of parameters

        Returns
        -------
        response: Response object with HTTP status and data set.

        """
        return super()._list(request, *args, **kwargs)



