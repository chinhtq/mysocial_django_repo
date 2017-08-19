from django import forms

from post.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'message','group')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'message': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'author', 'message'}

        widget = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'message': forms.Textarea(attrs={'class': 'editable medium-editor-textarea '})

        }
