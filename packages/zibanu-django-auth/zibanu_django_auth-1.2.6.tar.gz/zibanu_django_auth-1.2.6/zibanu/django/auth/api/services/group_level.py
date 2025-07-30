# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2024. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2024. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         11/05/24
# Project:      Zibanu Django
# Module Name:  group_level
# Description:
# ****************************************************************
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from zibanu.django.auth.lib import GroupLevelEnum
from zibanu.django.rest_framework.viewsets import ViewSet
from typing import Optional


class GroupLevelService(ViewSet):
    """
    Class to get group levels list through REST service.
    """

    def list(self, request: Request, *args: Optional[tuple[str, ...]], **kwargs: Optional[dict[str, ...]]) -> Response:
        """

        Parameters
        ----------
        request : Request
            HTTP request object
        args : tuple[str, Any] | None
            Tuple with arguments. Optional
        kwargs : dict[str, Any] | None
            Dict with keywords arguments

        Returns
        -------
        response: Response
            Object response with HTTP status and data. 200 if ok.
        """
        data = []
        for level in GroupLevelEnum:
            data.append(
                {
                    "level": level.value,
                    "name": level.label
                }
            )
        return Response(status=status.HTTP_200_OK, data=data)