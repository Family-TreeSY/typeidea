# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    target = forms.CharField(max_length=180, widget=forms.widgets.HiddenInput)
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'rows': 6, 'cols': 88}))

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('亲！写长一点噢！！！！！')

    class Meta:
        model = Comment
        fields = [
            'target', 'nickname', 'email', 'website', 'content'
        ]
