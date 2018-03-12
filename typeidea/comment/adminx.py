# comment\admin.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin
# from django.contrib import admin
from django.utils.html import format_html

from .models import Comment
from django.urls import reverse
from .adminforms import CommentAdminForm



# class CommentAdmin(admin.ModelAdmin):
class CommentAdmin(object):
    form = CommentAdminForm
    list_display = ['target', 'nickname', 'created_time', 'email', 'website', 'content', 'operator']
    # list_filter = ['nickname']
    # search_fields = ['post', 'nickename']
    actions_on_top = True
    date_hierarchy = 'created_time'

    '''
    编辑页面
    '''
    # fieldsets = (
    #     ('基础设置', {
    #         'fields': (('nickname', 'post'),
    #                    'website',
    #                    'content',
    #                    'email',),
    #     }),
    #     ('高级设置', {
    #         'classes': ('collapse', 'addon'),
    #         'fields': ('website',)
    #     })
    # )
    # fields = (('nickname', 'post'),
    #           'website',
    #           'email',
    #           'content')
    #
    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:comment_comment_change', args=(obj.id,))
        )

    operator.short_description = '操作'
xadmin.site.register(Comment, CommentAdmin)

