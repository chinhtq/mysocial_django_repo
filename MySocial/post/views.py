# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model

from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import  get_object_or_404

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, DeleteView

from post.form import CommentForm, PostForm
from post.models import Post
from groups.models import Group

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

    def get_context_data(self, **kwargs):

        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_success_url(self):
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


class CreatePost(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = "post/post_detail.html"
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        print self.request.user.pk
        group = get_object_or_404(Group, name= form.cleaned_data['group'])
        user = get_object_or_404(User, pk=self.request.user.pk)
        print  user.has_perm('can_post', group)
        print user
        print user.has_perm('can_post', group)
        if user.has_perm('can_post', group):
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            return super(CreatePost, self).form_valid(form)
        else:
            return HttpResponse("Permission to add denied")


class DeletePost(LoginRequiredMixin, DeleteView, SelectRelatedMixin):
    model = Post
    select_related = ("user", "group")
    success_url = reverse_lazy("post:user")

    def get_queryset(self):
        queryset = super(DeletePost, self).get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super(DeletePost, self).delete(*args, **kwargs)