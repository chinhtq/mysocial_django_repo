# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from braces.views import SelectRelatedMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, DeleteView

from groups.models import Group
from .form import CommentForm
from .models import Post

from .form import PostForm

User = get_user_model()


class PostList(SelectRelatedMixin, ListView):
    model = Post
    select_related = ("user", "group")


class UserPost(ListView):
    model = Post
    template_name = 'post/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super(UserPost, self).get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context


class PostDetail(DetailView, FormMixin):
    model = Post
    form_class = CommentForm
    login_url = '/login/'

    def get_context_data(self, **kwargs):

        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
        print self.object.user.username
        print self.object.pk
        return reverse('post:single', kwargs={'username': self.object.user.username, 'pk': self.object.pk})

    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']

        post = self.object
        print post
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

        return super(PostDetail, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CreatePost(SelectRelatedMixin, CreateView):
    redirect_field_name = 'post/post_detail.html'
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.request.user.pk)
        group = get_object_or_404(Group, name=form.cleaned_data['group'])
        print user.has_perm('groups.can_post', group)
        if user.has_perm('groups.can_post', group):
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            return super(CreatePost, self).form_valid(form)
        else : return reverse('post:post_user', kwargs={'username': self.request.user.username})


class DeletePostView(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    model = Post
    select_related = ("user", "group")

    def get_success_url(self):
        return reverse('post:post_user', kwargs={'username': self.object.user.username})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super(DeletePostView, self).delete(request, *args, **kwargs)
