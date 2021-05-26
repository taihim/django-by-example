from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

# Can give a different name to the tag using the name attribute
# @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts():
    return Post.published.count()

# Inclusion tags need to return a dict of values which is used as the context
# to render the specified template
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')
                            ).order_by('-total_comments')[:count]

# This converts markdown to html for easy dynamic rendering in templates
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))