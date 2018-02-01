# config/admin.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .adminforms import LinkAdminForm, SideBarAdminForm
from django.utils.html import format_html
from django.urls import reverse

from .models import Link, SideBar
from typeidea.custom_site import custom_site


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    form = LinkAdminForm
    list_display = [
        'title',
        'href',
        'status',
        'weight_show',
        'owner',
        'created_time',
        'operator']
    list_filter = ['title', 'owner']
    actions_on_top = True
    search_fields = [
        'title', 'href', 'owner',
    ]
    date_hierarchy = 'created_time'

    '''
    编辑页面
    '''
    fieldsets = (
        ('基础设置', {
            'fields': (('title', 'owner'),
                       'href',
                       'status',)
        }),
        ('高级设置', {
            'classes': ('collapse', 'addon'),
            'fields': ('weight',),
        }),
    )
    # 增加展示页面编辑按钮

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:config_link_change', args=(obj.id,))
        )

    operator.short_description = '操作'


@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    form = SideBarAdminForm
    list_display = [
        'title',
        'display_type',
        'content',
        'owner',
        'created_time',
        'operator']
    list_filter = ['title', 'owner']
    search_fields = ['title', 'owner']
    date_hierarchy = 'created_time'

    '''
    编辑页面
    '''
    fieldsets = (
        ('基础设置', {
            'fields': (('title', 'owner'),
                       'content',)
        }),
        ('高级设置', {
            'classes': ('collapse', 'addon'),
            'fields': ('display_type',)
        }),
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:config_sidebar_change', args=(obj.id,))
        )
