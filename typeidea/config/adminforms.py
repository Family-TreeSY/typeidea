# config/adminforms.py
# -*- coding: utf-8 -*-

from django import forms


class LinkAdminForm(forms.ModelForm):
    title = forms.CharField(widget=forms.Textarea, label='标题', required=False)


class SideBarAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='内容', required=False)