from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

# Create your views here.

# Class based alternative to the post_list function below
# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


# A Django view is a function that receives a web request
# and returns a response

# The request param is required by all views
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    # The paginator class can be used to split results into pages
    paginator = Paginator(object_list, 3) # 3 results per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver the 1st page 
        posts = paginator.page(1)

    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)


    # List of active comments for post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was POSTED
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # Create comment but don't save to database yet
            # The save() method creates an instance of the model that the form is linked
            # to and saves it to DB. The commit attribute controls whether it is saved.
            new_comment = comment_form.save(commit=False)
            # Assign current post to comment
            new_comment.post = post
            #Save commit to DB
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Gets the ids of the tags associated with this post
    # The flat attribute turns the result into a list of values instead of one-tuples
    # The annotate function allows us to create a calculated field 'same_tags' using
    # the Count aggregation function. 'same_tags' contains the number of tags shared 
    # with all the tags queried
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]


    return render(request, 'blog/post/detail.html',{'post': post, 
                                                    'comments': comments, 
                                                    'comment_form': comment_form, 
                                                    'new_comment': new_comment, 
                                                    'similar_posts': similar_posts})



def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # Builds complete URL including the HTTP schema and hostname
            # post.get_absolute_url() doesnt get the hostname or port
            # need to use request.build_absolute_uri for that
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"

            message = f"Read {post.title} at {post_url}\n\n " \
                      f"{cd['name']}\'s comments: {cd['comments']}"

            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent':sent})