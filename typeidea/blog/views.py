# blog/views.py
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from django.views.generic import ListView, DetailView


from .models import Post, Tag, Category
from config.models import SideBar
from comment.models import Comment
from comment.forms import CommentForm


class CommonMixin(object):
    def get_category_data(self):
        '''
        分类视图
        '''
        categories = Category.objects.filter(
            status=1)  # TODO: fix magic number
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

        return {
            'cates': cates,
            'nav_cates': nav_cates,
        }


    def get_sidebar_data(self):
        sidebars = SideBar.objects.filter(status=1)
        return {
            'sidebars': sidebars,
        }



    def get_context_data(self, **kwargs):
        # context = super(CommonMixin, self).get_context_data()
        # '''
        # 分类视图
        # '''
        # categories = Category.objects.filter(
        #     status=1)  # TODO: fix magic number
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

               # '''
        # 侧边视图
        # '''
        sidebars = SideBar.objects.filter(status=1)

        '''
        1.
        最近评论
        2.
        最近文章
        '''
        recently_posts = Post.objects.filter(status=1)[:10]
        # recently_comments = Comment.objects.filter(status=1)[:10]

        # context = {
        #     # 'nav_cates': nav_cates,
        #     # 'cates': cates,
        #     # 'sidebars': sidebars,
        #     'recently_posts': recently_posts,
        #     'recently_comments': recently_comments,
        # }
        kwargs.update({
            # 'nav_cates': nav_cates,
            # 'cates': cates,
            'sidebars': sidebars,
            'recently_posts': recently_posts,
            # 'recently_comments': recently_comments,
        })
        # context.update(extra_context)
        kwargs.update(self.get_category_data())
        # kwargs.update(self.get_sidebar_data())
        return super(CommonMixin, self).get_context_data(**kwargs)

class BasePostsView(CommonMixin, ListView):
    '''
    model: 告诉Django我们要获取的模型是Post
    template_name: 指定模板
    context_object_name: 注意看list.html中关于文章列表的变量名
    '''
    model = Post
    # template_name = 'themes/default/blog/list.html'
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3


class IndexView(BasePostsView):
    '''
    增加搜索功能
    1.数据过滤
    2.数据传递到模板里
    '''
    def get_queryset(self):
        query = self.request.GET.get('query')
        qs = super(IndexView, self).get_queryset()
        if query:
            qs = qs.filter(title__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        query = self.request.GET.get('query')
        return super(IndexView, self).get_context_data(query=query)



class CategoryView(BasePostsView):
    def get_queryset(self):
        qs = super(CategoryView, self).get_queryset()
        cate_id = self.kwargs.get('category_id')
        qs = qs.filter(category_id=cate_id)
        return qs


class TagView(BasePostsView):
    def get_queryset(self):
        tag_id = self.kwargs.get('tag_id')
        try:
            tag = Tag.objects.get(pk=tag_id)
        except Tag.DoesNotExist:
            return []

        posts = tag.posts.all()
        return posts


class AuthorView(BasePostsView):
    def get_queryset(self):
        author_id = self.kwargs.get('author_id')
        qs = super(AuthorView, self).get_queryset()
        if author_id:
            qs = qs.filter(owner_id=author_id)
        return qs


class PostView(CommonMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        kwargs.update({
            'comment_form': CommentForm(),
        })
        return super(PostView,self).get_context_data(**kwargs)

    # def get_sidebar_data(self):
    #     return []


# def get_common_context():
#     '''
#     分类视图
#     '''
#     categories = Category.objects.filter(status=1)  # TODO: fix magic number
#     '''
#     1. 导航分类和普通分类
#     nav_cates = categories.filter(is_nav=True)
#     cates = categories.filter(is_nav=False)
#
#     2.
#     nav_cates = [cate for cate in categories if cate.is_nav]
#     cates = [cate for cate in categories if not cate.is_nav]
#     '''
#
#     nav_cates = []
#     cates = []
#     for cate in categories:
#         if cate.is_nav:
#             nav_cates.append(cate)
#         else:
#             cates.append(cate)
#
#     '''
#     侧边视图
#     '''
#     sidebars = SideBar.objects.filter(status=1)
#
#     '''
#     1.
#     最近评论
#     2.
#     最近文章
#     '''
#     recently_posts = Post.objects.filter(status=1)[:10]
#     recently_comments = Comment.objects.filter(status=1)[:10]
#
#     context = {
#         'nav_cates': nav_cates,
#         'cates': cates,
#         'sidebars': sidebars,
#         'recently_posts': recently_posts,
#         'recently_comments': recently_comments,
#     }
#     return context


# def post_list(request, category_id=None, tag_id=None):
#     '''
#     文章列表视图
#     :param request:
#     :param category_id:
#     :param tag_id:
#     :return:
#     '''
#     queryset = Post.objects.all().order_by('-created_time')
#     # 从第一页开始
#     page = request.GET.get('page', 1)
#     # 每页数据数量
#     page_size = 3
#     try:
#         page = int(page)
#     except TypeError:
#         page = 1
#     if category_id:
#         queryset = queryset.filter(category_id=category_id)
#     elif tag_id:
#         try:
#             tag = Tag.objects.get(id=tag_id)
#         except Tag.DoesNotExist:
#             queryset = []
#         else:
#             queryset = tag.posts.all()
#
#     paginator = Paginator(queryset, page_size)
#     try:
#         posts = paginator.page(page)
#     except EmptyPage:  # 页面超过页数范围就传递最后一页数据
#         posts = paginator.page(paginator.num_pages)

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

#     context = {
#         'posts': posts,
#         # 'nav_cates': nav_cates,
#         # 'cates': cates,
#         # 'sidebars': sidebars,
#         # 'recently_posts': recently_posts,
#         # 'recently_comments': recently_comments,
#     }
#     # 调用get_common_text()方法，更新context
#     common_context = get_common_context()
#     context.update(common_context)
#     return render(request, 'blog/list.html', context=context)
#
#
# def post_detail(request, pk=None):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         raise Http404('Post does not exist!')
#     context = {
#         'post': post,
#     }
#     # 调用get_common_text()方法，更新context
#     common_context = get_common_context()
#     context.update(common_context)
#     return render(request, 'blog/detail.html', context=context)
