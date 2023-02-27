from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', 
        views.PostDetail.as_view(), 
        name='post_detail'
    ),
    path('<int:post_id>/share/',
        views.PostShare.as_view(), 
        name='post_share'
    ),
    path('<int:post_id>/comment/',
        views.PostComment.as_view(), 
        name='post_comment'
    ),
    path('tag/<slug:tag_slug>/',
        views.PostListView.as_view(),
        name='post_list_by_tag'
    ),
    path(
        'feed/', LatestPostsFeed(), name='post_feed'
    ),
    path(
        'search/', views.PostSearch.as_view(), name='post_search'
    )
]
