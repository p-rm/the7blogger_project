from django import forms
from django.contrib.auth.models import User
from models import Post, Comment
from time import time

#def get_upload_path_file_name(instance, filename):
#    return 'user-files/%s_%s' % (str(time()).replace('.', '_'), filename)

class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}), label='')
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Quote'}), label='')
    photo = forms.FileField(label='')
    #photo = forms.FileField(upload_to=get_upload_path_file_name, label='')

    class Meta:
        model = Post
        fields = ('title', 'body', 'photo')


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your feedback'}), label='')

    class Meta:
        model = Comment
        fields = ('body', )