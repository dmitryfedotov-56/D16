from .models import *
from django import forms
from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'content']


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['text']

    def get_form_kwargs(self):
        kwargs = super(CommentForm, self).get_form_kwargs()
        return kwargs


class PostUpdateForm(ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'content']