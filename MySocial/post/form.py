from django import forms

from . import models
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'message', 'group')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'message': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop("user", None)
            print "Username " + user.username
            print user.groups.values_list("group__pk")
            super(PostForm, self).__init__(*args, **kwargs)
            if user is not None:
                self.fields["group"].queryset = (
                    models.Group.objects.filter(

                    )
                )
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'author', 'message'}

        widget = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'message': forms.Textarea(attrs={'class': 'editable medium-editor-textarea '})

        }
