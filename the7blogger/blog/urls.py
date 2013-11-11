from django.conf.urls import patterns, include, url

urlpatterns = patterns('blog.views',
    url(r'^the-dashboard/$', 'the_dashboard', name='the_dashboard'),
    url(r'^my-posts/$', 'my_posts', name='my_posts'),
    url(r'^new-post/$', 'new_post', name='new_post'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$', 'post_get_by_slug', name='post_get_by_slug'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/like/$', 'post_like', name='post_like'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/comments/$', 'post_comments', name='post_comments'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/delete-comment/(?P<pk>\d+)/$', 'delete_comment',
        name='delete_comment'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/delete-all-comments/$', 'delete_comment',
        name='delete_comment'),

    #url(r'^like/(?P<post_id>\d+)/$', 'post_like', name='post_like'),
    #url(r'^add-comment/(?P<post_id>\d+)/$', 'post_add_comment', name='post_add_comment'),
    url(r'^([-\w]+)/$', 'post_get', name='post_get'),




)