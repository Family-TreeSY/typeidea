# blog/adminforms.py
# -*- coding: utf-8 -*-
from dal import autocomplete
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Category, Tag, Post


class PostAdminForm(forms.ModelForm):
    # status = forms.BooleanField(label='是否删除', required=True) #TODO: 处理布尔类型为我们需要的字段
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    content = forms.CharField(widget=CKEditorWidget(), label='内容')
    category = forms.ModelChoiceField(
            queryset=Category.objects.all(),
            widget=autocomplete.ModelSelect2(url='category-autocomplete'),
            label='分类',
        )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签',
    )

    #wwdwww
    # class Mata:
    #     model = Post
    #     fields = (
    #         'title',
    #         'desc',
    #         ('category', 'tag', 'status'),
    #         ('content', 'is_markdown'),
    #     )

# def clean_status(self):
#     if self.cleaned_data['status']:
#         return 1
#     else:
#         return 2
