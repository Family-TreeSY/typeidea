# blog/admin.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import xadmin
from xadmin.layout import Fieldset, Row
# from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Tag, Post
# from typeidea.custom_site import custom_site
from .adminforms import PostAdminForm
from typeidea.adminx import BaseOwnerAdmin


# class PostAdmin(admin.ModelAdmin):
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = [
        'title',
        'category',
        'status_show',
        'pv',
        'uv',
        'owner',
        'created_time',
        'operator']
    # category、status变为可点链接
    # list_display_links = ['category', 'status_show', 'title']
    search_fields = ['title', 'category__name', 'owner__username']
    list_filter = ['owner']
    # 动作按钮在上
    actions_on_top = True
    # 动作按钮在底部
    actions_on_bottom = False
    # 创建时间
    date_hierarchy = 'created_time'
    # 展示可编辑项
    # list_editable = ['title']

    '''
    编辑页面
    '''
    # 增加删除保存键置顶
    # save_on_top = True
    # 要展示的字段
    # fields = (
    #     'title', 'category',
    #     'tag',
    #     'desc',
    #     'status',
    #     'content', 'is_markdown',
    # )
    exclude = (
        'html', 'owner', 'html', 'pv', 'uv',
    )
    form_layout = (
        Fieldset(
            "基础信息",
            'title',
            'desc',
            Row('category', 'tag', 'status'),
            'is_markdown',
            'content',
        ),
    )
    #

    # status不展示
    # exclude = ('status',)
    # fieldsets = (  # 跟fields互斥
    #     ('基础设置', {
    #         'fields': (('category', 'title'),
    #                    'desc',
    #                    'status',  # TODO(Treehl): 后面添加的字段
    #                    'content')
    #     }),
    #     ('高级设置', {
    #         'classes': ('collapse', 'addon'),
    #         'fields': ('tag',),
    #     }),
    # )
    # 水平布局
    # filter_horizontal = ('tag', )
    # 垂直布局
    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'
xadmin.site.register(Post, PostAdmin)
# xadmin.site.register(Post, PostAdmin)

    # def save_model(self, request, obj, form, change):
    #     print self, request, obj, form, change
    #     obj.owner = request.user
    #     super(PostAdmin, self).save_model(request, obj, form, change)


# class PostInline(admin.TabularInline):
#     fields = ('title', 'desc', 'status')
#     extra = 2  # 控制额外多几个
#     # 指定模型类
#     model = Post


# class CategoryAdmin(admin.ModelAdmin):
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ['name', 'status', 'is_nav', 'created_time', 'operator']
    fields = ('name', 'status', 'is_nav')

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_category_change', args=(obj.id,))
        )

    operator.short_description = '操作'
xadmin.site.register(Category, CategoryAdmin)

# class TagAdmin(admin.ModelAdmin):
class TagAdmin(BaseOwnerAdmin):
    list_display = ['name', 'status', 'created_time', 'operator']
    fields = ('name', 'status')

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_tag_change', args=(obj.id,))
        )
    operator.short_description = '操作'
xadmin.site.register(Tag, TagAdmin)



