# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2024. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2024. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: Mario Cerón Charry
# Date:         19/08/23 15:09
# Project:      Zibanu - Django
# Module Name:  auth
# Description:  
# ****************************************************************
import logging
import traceback

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.models import TokenUser

from zibanu.django.auth.lib.utils import get_cache_key
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.viewsets import ViewSet
from zibanu.django.lib.utils import get_user


class LogoutUser(ViewSet):
    """
    ViewSet to perform logout actions and remove cached tokens.
    """

    def logout(self, request, *args, **kwargs) -> Response:
        user = get_user(request.user)

        if isinstance(request.user, TokenUser) and hasattr(request.user, "token"):
            token = request.user.token
            token.blacklist()

        try:
            if not user.is_superuser and hasattr(user, "profile"):
                cache_key = get_cache_key(request, user)
                cache.delete(cache_key)
        except Exception as exc:
            logging.error(str(exc))
            logging.debug(traceback.format_exc())
            raise APIException() from exc
        finally:
            return Response(status=status.HTTP_200_OK)
