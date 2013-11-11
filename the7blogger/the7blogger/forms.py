from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='', required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='', required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}), label='', required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}), label='', required=True)

    class Meta:  # which other objects exist on the form
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        #widgets = {'username': forms.TextInput(attrs={'placeholder': ' ? Username'}),
        #           'password1': forms.TextInput(attrs={'placeholder': ' ? Password'}),
        #           'password2': forms.TextInput(attrs={'placeholder': ' ? Repeat password'}),
        #           'email': forms.TextInput(attrs={'placeholder': ' ? Email'}),
        #          }

    def save(self, commit=True):
        user = super(CustomRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}), label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label='', required=True)

    class Meta:
        model = User
        fields = ('username', 'password')
        #widgets = {'username': forms.TextInput(attrs={'placeholder': ' ? Username'}),
        #           'password': forms.TextInput(attrs={'placeholder': ' ? Password'}),
        #           }
