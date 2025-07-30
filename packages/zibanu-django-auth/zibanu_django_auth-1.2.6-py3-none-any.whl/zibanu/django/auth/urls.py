# -*- coding: utf-8 -*-

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/04/23 7:32
# Project:      Django Plugins
# Module Name:  urls
# Description:
# ****************************************************************
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainSlidingView
from rest_framework_simplejwt.views import TokenRefreshSlidingView
from zibanu.django.auth.api.services import GroupService
from zibanu.django.auth.api.services import GroupLevelService
from zibanu.django.auth.api.services import LogoutUser
from zibanu.django.auth.api.services import PermissionService
from zibanu.django.auth.api.services import ProfileService
from zibanu.django.auth.api.services import UserService

"""
URL patterns for zibanu.django.auth package
"""

urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="Get a new token from credentials."),
    path("logout/", LogoutUser.as_view({"post": "logout"}), name="Logout user endpoint."),
    path("refresh/", TokenRefreshSlidingView.as_view(), name="Refresh token."),
    path("change-password/", UserService.as_view({"post": "change_password"}), name="Change current password."),
    path("request-password/", UserService.as_view({"post": "request_password"}), name="Request a new password."),
    path("group/list/", GroupService.as_view({"post": "list"}), name="Group users list."),
    path("grouplevel/list/", GroupLevelService.as_view({"post": "list"}), name="Group level service."),
    path("permission/list/", PermissionService.as_view({"post": "list"}), name="Permissions list."),
    path("profile/update/", ProfileService.as_view({"post": "update"}), name="Update user's profile."),
    path("user/add/", UserService.as_view({"post": "create"}), name="Create a new user."),
    path("user/avatar/", UserService.as_view({"post": "get_avatar"}), name="Get user's avatar."),
    path("user/delete/", UserService.as_view({"post": "destroy"}), name="Delete user."),
    path("user/list/", UserService.as_view({"post": "list"}), name="Users list"),
    path("user/profile/", UserService.as_view({"post": "get_profile"}), name="Get user's profile."),
    path("user/retrieve/", UserService.as_view({"post": "retrieve"}), name="Get user."),
    path("user/update/", UserService.as_view({"post": "update"}), name="Update user.r")
]