from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from time import time

def get_upload_path_file_name(instance, filename):
    return 'user-files/%s_%s' % (str(time()).replace('.', '_'), filename)


#TODO field to add photo details!

class Post(models.Model):
    title = models.CharField(max_length=60, unique=True)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    photo = models.FileField(upload_to=get_upload_path_file_name)
    user = models.ForeignKey(User)
    slug = models.SlugField(unique=True)

    def save(self):
        if not self.id:
            #new object, create slug
            super(Post, self).save()
            self.slug = '%i-%s' % (self.id, slugify(self.title))
        super(Post, self).save()

    def __str__(self):
        return self.title

    def get_created_as_string(self):
        dt = self.created.strftime("%B %d, %Y")
        return dt

    #for testing purposes
    #@models.permalink
    def get_absolute_url_2(self):
        #return "/blog/get/%i/" % self.id
        #url = reverse("blog.views.post_get", args=str(self.id), kwargs={'post_id': str(self.id)})
        url = reverse("post_get", args=[str(self.id)])
        return url

    def get_absolute_url(self):
        d = dict()
        d = {'year': str(self.created.year), 'month': str(self.created.strftime('%m')), 'slug': str(self.slug)}
        return reverse('blog:post_get_by_slug', kwargs=d)



class Comment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
    #TODO: add comment likes

    def __str__(self):
        return self.author

#TODO profiles
