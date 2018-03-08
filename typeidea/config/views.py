# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from blog.views import CommonMixin
from .models import Link
# from comment.views import Comment
# from comment.forms import CommentForm
from comment.views import CommentShowMixin

class LinkView(CommonMixin, CommentShowMixin, ListView):
    queryset = Link.objects.filter(status=1)
    model = Link
    template_name = 'config/links.html'
    context_object_name = 'links'

    # def get_comment(self):
    #     target = self.request.path
    #     comments = Comment.objects.filter(target=target)
    #     return comments
    #
    # def get_context_data(self, **kwargs):
    #     kwargs.update({
    #         'comment_form': CommentForm(),
    #         'comment_list': self.get_comment()
    #     })
    #     return super(LinkView, self).get_context_data(**kwargs)