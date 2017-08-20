# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from django.utils import timezone
import misaka

from django.contrib.auth import get_user_model

from groups.models import Group
import re
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts")
    title = models.CharField(max_length=200, default='')
    created_at = models.DateTimeField(default=timezone.now())
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name="posts", null=True, blank=True,)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "post:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk,
            }
        )

    class Meta:
        ordering = ["created_at"]
        unique_together = ["user", "message"]



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments")
    author = models.CharField(max_length=200)
    message = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approve_comment = models.BooleanField(default=True)

    def approve(self):
        self.approve_comment = True
        self.save()

    def __str__(self):
        return self.message
