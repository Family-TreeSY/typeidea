# blog/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
# from django.http import HttpResponse

from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment


# Create your views here.

def get_common_context():
    '''
           分类视图
           '''
    categories = Category.objects.filter(status=1)  # TODO: fix magic number
    '''
    1. 导航分类和普通分类
    nav_cates = categories.filter(is_nav=True)
    cates = categories.filter(is_nav=False)

    2.
    nav_cates = [cate for cate in categories if cate.is_nav]
    cates = [cate for cate in categories if not cate.is_nav]
    '''

    nav_cates = []
    cates = []
    for cate in categories:
        if cate.is_nav:
            nav_cates.append(cate)
        else:
            cates.append(cate)

    '''
    侧边视图
    '''
    sidebars = SideBar.objects.filter(status=1)

    '''
    1.
    最近评论
    2.
    最近文章
    '''
    recently_posts = Post.objects.filter(status=1)[:10]
    recently_comments = Comment.objects.filter(status=1)[:10]

    context = {
        'nav_cates': nav_cates,
        'cates': cates,
        'sidebars': sidebars,
        'recently_posts': recently_posts,
        'recently_comments': recently_comments,
    }
    return context


def post_list(request, category_id=None, tag_id=None):
    '''
    文章列表视图
    :param request:
    :param category_id:
    :param tag_id:
    :return:
    '''
    queryset = Post.objects.all().order_by('-created_time')
    # 从第一页开始
    page = request.GET.get('page', 1)
    # 每页数据数量
    page_size = 3
    try:
        page = int(page)
    except TypeError:
        page = 1
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    elif tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            queryset = []
        else:
            queryset = tag.post_set.all()

    '''
    分页视图
    '''
    paginator = Paginator(queryset, page_size)
    try:
        posts = paginator.page(page)
    except EmptyPage:  # 页面超过页数范围就传递最后一页数据
        posts = paginator.page(paginator.num_pages)

    # print len(posts)
    # import pdb;pdb.set_trace()

    # '''
    # 分类视图
    # '''
    # categories = Category.objects.filter(status=1)  # TODO: fix magic number
    # '''
    # 1. 导航分类和普通分类
    # nav_cates = categories.filter(is_nav=True)
    # cates = categories.filter(is_nav=False)
    #
    # 2.
    # nav_cates = [cate for cate in categories if cate.is_nav]
    # cates = [cate for cate in categories if not cate.is_nav]
    # '''
    #
    # nav_cates = []
    # cates = []
    # for cate in categories:
    #     if cate.is_nav:
    #         nav_cates.append(cate)
    #     else:
    #         cates.append(cate)
    #
    # '''
    # 侧边视图
    # '''
    # sidebars = SideBar.objects.filter(status=1)
    #
    # '''
    # 1.
    # 最近评论
    # 2.
    # 最近文章
    # '''
    # recently_posts = Post.objects.filter(status=1)[:10]
    # recently_comments = Comment.objects.filter(status=1)[:10]

    context = {
        'posts': posts,
        # 'nav_cates': nav_cates,
        # 'cates': cates,
        # 'sidebars': sidebars,
        # 'recently_posts': recently_posts,
        # 'recently_comments': recently_comments,
    }
    # 调用get_common_text()方法，更新context
    common_context = get_common_context()
    context.update(common_context)
    return render(request, 'blog/list.html', context=context)


def post_detail(request, pk=None):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        raise Http404('Post does not exist!')
    context = {
        'post': post,
    }
    # 调用get_common_text()方法，更新context
    common_context = get_common_context()
    context.update(common_context)
    return render(request, 'blog/detail.html', context=context)
