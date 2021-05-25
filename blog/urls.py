from django.urls import path
from . import views

# Creating a urls.py file for each app is the best way
# to make the apps reusable


# Defines an application namespace allowing us to organize
# URLs by application and use the name when referring to them
app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    
    # Values in angled brackets are treated as variables and
    # passed as arguments to the attached view
    # the expected datatype can be specified before the colon
    # using path converters e.g. <int:> <slug:> <str:> etc
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'), 
]

