from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'the7blogger.views.home', name='home'),
                       # url(r'^the7blogger/', include('the7blogger.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),

                       #url(r'^$', 'the7blogger.views.home', name='home'),
                       # user auth urls

                       #url(r'^$', 'the7blogger.views.user_registration', name='user_registration'),
                       url(r'^$', 'blog.views.the_dashboard', name='the_dashboard'),
                       url(r'^registration/$', 'the7blogger.views.user_registration', name='user_registration'),
                       url(r'^login/$', 'the7blogger.views.user_login', name='user_login'),
                       url(r'^logout/$', 'the7blogger.views.user_logout', name='user_logout'),


)
