# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import  get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from guardian.shortcuts import assign_perm, remove_perm

from accounts.models import User
from groups import models
from groups.models import Group, GroupMember

User = get_user_model()


class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroups(DetailView):
    model = Group


class ListGroups(ListView):
    model = Group


class JoinGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, ("Warning, already a member of {}".format(group.name)))

        else:
            print self.request.user.pk
            user = get_object_or_404(User, pk=self.request.user.pk)
            assign_perm('can_post', user, group)
            user = get_object_or_404(User, pk=self.request.user.pk)
            print user.has_perm('can_post', group)
            messages.success(self.request, "You are now a member of the {} group.".format(group.name))
        return super(JoinGroup, self).get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get("slug"))
        try:
            membership = models.GroupMember.objects.filter(user=self.request.user,
                                                           group__slug=self.kwargs.get("slug")).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,
                             "Warning, You cant leave {} group because you aren't in it ".format(group.name))
        else:
            print self.request.user.pk
            user = get_object_or_404(User, pk=self.request.user.pk)
            remove_perm('can_post', user, group)
            user = get_object_or_404(User, pk=self.request.user.pk)
            print user.has_perm('groups.can_post', group)
            membership.delete()
            messages.success(self.request, "You have successfully left this group.")
        return super(LeaveGroup, self).get(request, *args, **kwargs)
