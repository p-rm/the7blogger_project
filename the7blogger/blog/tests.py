"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core.urlresolvers import reverse
from model_mommy import mommy
from .models import Post, Comment
from .views import *

from datetime import datetime

# python manage.py test blog -v 2
# coverage run manage.py test blog -v 2
# coverage report
# coverage html
# coverage report --omit django
# coverage report --omit="/home/paulo/Programs/google_appengine/lib/django-1.5/*" --omit="/home/paulo/.virtualenvs/the7blogger/lib/python2.7/site-packages/*"


class PostTest(TestCase):
    def create_post(self, title='test post', body='hello world'):
        return Post.objects.create(title=title, body=body, created=datetime.now(), likes=0)

    def test_post_creation(self):
        p = self.create_post()
        self.assertTrue(isinstance(p, Post))
        self.assertEqual(p.__str__(), p.title)

    def test_all_posts_view(self):
        #p = mommy.make(Post)
        p = self.create_post()
        url = reverse('my_wall')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn(p.title, response.content)

    def test_get_post_view(self):
        #p = mommy.make(Post)
        p = self.create_post()
        url = reverse('post_get', args=[p.id])
        response = self.client.get(url)

        self.assertEqual(reverse('post_get', args=[p.id]), p.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertIn(p.title, response.content)


# VIEWS
# using mommy for fixtures
class PostTest_mommy(TestCase):
    def test_post_creation(self):
        p = mommy.make(Post)
        self.assertTrue(isinstance(p, Post))
        self.assertEqual(p.__str__(), p.title)


class PostViewsTestCase(TestCase):
    def test_index(self):
        resp = self.client.get('/my_wall/')
        self.assertEqual(resp.status_code, 200)