from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse, resolve
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.context_processors import csrf

from forms import CustomRegistrationForm, CustomLoginForm


def user_login(request):
    context = dict()
    context.update(csrf(request))
    form = CustomLoginForm(request.POST or None)
    context['form'] = form

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        logged_in = try_to_login(request, username, password)
        if logged_in is True:
            return HttpResponseRedirect(reverse('blog:my_posts'))
        else:
            context['error_message'] = logged_in

    return render(request, 'login.html', context)


def user_registration(request):
    context = dict()
    context.update(csrf(request))
    form = CustomRegistrationForm(request.POST or None)
    context['form'] = form

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        if form.is_valid():
            form.save()
            logged_in = try_to_login(request, username, password)
            if logged_in is True:
                return HttpResponseRedirect(reverse('blog:my_posts'))
            else:
                context['error_message'] = logged_in

    return render(request, 'register.html', context)


def user_logout(request):
    auth.logout(request)
    try:
        del request.session['username']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('blog:the_dashboard'))


#/* Aux */

def try_to_login(request, username, password):
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth.login(request, user)
            request.session['username'] = username
            return True
        else:
            return 'Sorry, your account has been disabled'
    else:
        return 'Sorry, invalid login'