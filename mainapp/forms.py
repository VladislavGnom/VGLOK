from django import forms

from mainapp.models import PostVGUser, Comment

class PostVGUserForm(forms.ModelForm):
    class Meta:
        model = PostVGUser
        fields = ('description', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
