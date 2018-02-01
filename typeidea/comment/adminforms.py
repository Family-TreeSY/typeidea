# comment/adminforms.py
# -*- coding: utf-8 -*-

from django import forms


class CommentAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='内容', required=False)