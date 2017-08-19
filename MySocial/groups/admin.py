# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from groups.models import Group, GroupMember


class GroupMemberInline(admin.TabularInline):
    model = GroupMember


admin.site.register(Group)
admin.site.register(GroupMember)
