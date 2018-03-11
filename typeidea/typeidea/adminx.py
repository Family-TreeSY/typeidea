# -*- coding: utf-8 -*-

from __future__ import unicode_literals

# from django.contrib import admin
import xadmin
from xadmin.views import CommAdminView

class BaseOwnerAdmin(object):
    '''
    1. save_model - 保证每条数据都属于当前用户
    2. 重写get_queryset - 保证每个用户只能看到自己的文章

    '''

    def get_list_queryset(self):
        request = self.request
        qs = super(BaseOwnerAdmin, self).get_list_queryset()
        # 是超级用户返回qs
        if request.user.is_superuser:
            return qs
        # 不是返回自己用户
        return qs.filter(owner=request.user)

    def save_models(self):
        # import pdb;pdb.set_trace()
        if not self.org_obj:
            self.new_obj.owner = self.request.user
        return super(BaseOwnerAdmin, self).save_models()

class GlobalSetting(CommAdminView):
    site_title = 'TypeIdea管理后台'
    site_footer = 'power by typeidea@treehl'

xadmin.site.register(CommAdminView, GlobalSetting)
