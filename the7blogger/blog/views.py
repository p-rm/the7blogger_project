# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse, resolve
from django.core.context_processors import csrf
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from forms import PostForm, CommentForm
from .models import Post, Comment

import datetime


def hello(request):
    return HttpResponse('Hello World!')


def the_dashboard(request):
    now = datetime.datetime.now()
    context = dict()
    posts = Post.objects.all().order_by("-likes", "-created")[:7]

    context['current_date']=now
    context['posts']=posts
    return render(request, 'the_dashboard.html', context)


@login_required
def my_posts(request):
    now = datetime.datetime.now()
    context = dict()
    u = User.objects.get(username=request.user.username)
    posts = Post.objects.filter(user=u.id).order_by("-created")

    paginator = Paginator(posts, 1)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    context['current_date']=now
    context['posts']=posts
    return render(request, 'my_posts.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            u = User.objects.get(username=request.user.username)
            new_post.user = u
            new_post.save()

            return HttpResponseRedirect(reverse('blog:my-posts'))

    else:
        form = PostForm()

    context = dict()
    context.update(csrf(request))
    context['form'] = form
    return render(request, 'new_post.html', context)



@login_required
def post_get(request, post_id=None):
    context = dict()
    post = Post.objects.get(id=post_id)
    context['post']=post
    return render(request, 'post_get.html', context)


@login_required
def post_get_by_slug(request, year, month, slug):
    context = dict()
    #TODO by user?! for the moment the slug contains id
    post = Post.objects.get(created__year=int(year), created__month=int(month), slug=slug)
    if not post:
        raise Http404

    context['post']=post
    return render(request, 'post_get_by_slug.html', context)


@login_required
def post_comments(request, year, month, slug):
    context = dict()
    context.update(csrf(request))
    now = datetime.datetime.now()
    if year and month and slug:
        post = Post.objects.get(created__year=int(year), created__month=int(month), slug=slug)

        form = CommentForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                comment = form.save(commit=False)
                u = User.objects.get(username=request.user.username)
                comment.author = u
                comment.created = now
                comment.post = post
                comment.save()
                form = CommentForm()
                #TODO maybe should got to blog/year/month/slug
                #return HttpResponseRedirect('/blog%s' % post.get_absolute_url())

    comments = Comment.objects.filter(post=post).order_by("-created")

    context['post'] = post
    context['comments'] = comments
    context['form'] = form
    return render(request, 'post_comments.html', context)


@login_required
#def delete_comment(request, year, month, slug, pk=None):
def delete_comment(request, *args, **kwargs):
    context = dict()
    for key in kwargs:
        context[key] = str(kwargs[key])

    if context['year'] and context['month'] and context['slug']:
        post = Post.objects.get(created__year=int(context['year']), created__month=int(context['month']), slug=context['slug'])

        if request.user.is_staff or post.user.username == request.user.username:
            if 'pk' not in context:
                pk_list = request.POST.getlist('delete')
            else:
                pk_list = [context['pk']]

        for pk in pk_list:
            Comment.objects.get(pk=pk).delete()

        # url does not contain 'pk' key, needs to be removed from dict
        if 'pk' in context:
            del context['pk']

        return HttpResponseRedirect(reverse('blog:post_comments', kwargs=context))
    else:
        return HttpResponseRedirect(reverse('blog:my-posts'))


@login_required
def post_like(request, year, month, slug):
    if year and month and slug:
        post = Post.objects.get(created__year=int(year), created__month=int(month), slug=slug)
        key = 'has_liked_%s' % post
        if request.session.get(key, False):
            try:
                post.likes -= 1
                del request.session[key]
            except KeyError:
                pass
        else:
            post.likes += 1
            request.session[key] = True
        post.save()

        try:
            page = int(request.GET.get('page', 0))
        except ValueError:
            page = 0

        if page == 0:
            return HttpResponseRedirect(post.get_absolute_url())
        else:
            return HttpResponseRedirect('/blog/my-posts/?page=%d' % page)
