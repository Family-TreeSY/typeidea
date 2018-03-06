# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from blog.views import CommonMixin
from .models import Link

class LinkView(CommonMixin, ListView):
    queryset = Link.objects.filter(status=1)
    model = Link
    template_name = 'config/links.html'
    context_object_name = 'links'