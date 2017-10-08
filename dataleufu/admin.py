# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib.gis import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserGroup

class CustomUserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'usuarios'

class UserProfileAdmin(UserAdmin):
    inlines = (CustomUserInline, )


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(UserGroup)
