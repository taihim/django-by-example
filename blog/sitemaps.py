from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    # Both the changefreq and priority attributes can either be methods or 
    # attributes
    changefreq = 'weekly'
    priority = 0.9

    # The items method returns the QuerySet of objects to include in this sitemap
    # By default, Django calls the get_absolute_url method on each object to retrieve
    # its URl
    def items(self):
        return Post.published.all()

    # The lastmod method receives each object returned by items() and returns
    # the last time the object was modified
    def lastmod(self, obj):
        return obj.updated