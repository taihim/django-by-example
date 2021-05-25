from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .forms import EmailPostForm
from django.core.mail import send_mail

# Create your views here.

# Class based alternative to the post_list function below
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# A Django view is a function that receives a web request
# and returns a response

# The request param is required by all views
# def post_list(request):
#     object_list = Post.published.all()

#     # The paginator class can be used to split results into pages
#     paginator = Paginator(object_list, 3) # 3 results per page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)

#     except PageNotAnInteger:
#         # If page is not an integer, deliver the 1st page 
#         posts = paginator.page(1)

#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)

#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)

    return render(request, 'blog/post/detail.html',{'post':post})



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