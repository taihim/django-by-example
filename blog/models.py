from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# django-taggit package for adding tags to models
# pip install django-taggit
from taggit.managers import TaggableManager

# Create your models here.

# The first manager defined in a model becomes the default manager
class PublishedManager(models.Manager):
    # The get_queryset() method of a manager returns the 
    # queryset that will be executed. You override this 
    # method to include your custom filter in the final 
    # QuerySet.
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    # We can specify multiple managers for our model
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    
    
    author = models.ForeignKey(User, 
                                on_delete=models.CASCADE,
                                related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')

    #class that contains metadata
    class Meta:
        #controls the order in which results are fetched from db
        #currently, results are ordered by publish date in descending order
        ordering = ('-publish',)
        
        #used to set the name of the created table
        #default name is 'appname_modelname' i.e. blog_post in this case
        #but we can set it to anything we want using this variable
        db_table = 'blog_post'


    #default human-readable representation of the object
    #used in many places by django, such as admin site
    def __str__(self):
        return self.title

    # The reverse function takes a view and the values of
    # the args it expects and returns the final URL
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day, self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Comment by {} on {}".format(self.name, self.post)
