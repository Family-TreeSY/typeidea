# blog/models.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Category(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=1, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    STATUS_ITEMS = (
        (1, '正常'),
        (2, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(
        default=1, choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __unicode__(self):
        return self.name


class Post(models.Model):
    STATUS_ITEMS = (
        (1, '上线'),
        (2, '删除'),
        # (3, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name='标题')
    pv = models.PositiveIntegerField(default=0, verbose_name='pv')
    uv = models.PositiveIntegerField(default=0, verbose_name='uv')
    desc = models.CharField(max_length=255, blank=True, verbose_name='摘要')
    content = models.TextField(verbose_name='正文', help_text='正文必须为MarkDown格式')
    html = models.TextField(verbose_name='html渲染后的页面', default='', help_text='正文必须为MarkDown格式')
    is_markdown = models.BooleanField(verbose_name='使用markdown', default=True)
    status = models.PositiveIntegerField(
        default=1, choices=STATUS_ITEMS, verbose_name='状态')
    category = models.ForeignKey(Category, verbose_name='分类')
    tag = models.ManyToManyField(Tag, related_name='posts', verbose_name='标签')
    owner = models.ForeignKey(User, verbose_name='作者')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def status_show(self):
        return '当前状态: %s' % self.status
    status_show.short_description = '展示状态'

    def __unicode__(self):
        return self.title

    def increase_pv(self):
        return type(self).objects.filter(id=self.id).update(pv=F('pv') + 1)

    def increase_uv(self):
        return type(self).objects.filter(id=self.id).update(uv=F('uv') + 1)

    def save(self, *args, **kwargs):
        if self.is_markdown:
            # config = {
            #     'codehilite': {
            #         'use_pygments': True,
            #         'css_class': 'prettyprint linenums',
            #     }
            #
            # }
            # self.html = markdown.markdown(self.content, extensions=['codehilite'], extension_configs=config)
            self.html = markdown.markdown(self.content, extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
        else:
            self.html = self.content
        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']