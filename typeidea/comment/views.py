# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import TemplateView

from .forms import CommentForm


class CommentView(TemplateView):
    template_name = 'comment/result.html'

    def get(self, request, *args, **kwargs):
        return super(CommentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # TODO: 获取path
        target = request.POST.get('target')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save(commit=False)
            succeed = True
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
        }
        return self.render_to_response(context)
