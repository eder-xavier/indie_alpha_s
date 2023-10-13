from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'storage_app'

urlpatterns = [
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('toggle_follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),

    path('friend_requests/', views.friend_requests, name='friend_requests'),
    
    path('add_comment/<int:publication_id>/', views.add_comment, name='add_comment'),
    path('get_comment_count/<int:publication_id>/', views.get_comment_count, name='get_comment_count'),
    path('view_comments/<int:publication_id>/', views.view_comments, name='view_comments'),
    path('reply_to_comment/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('files/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('userprofile/<int:user_id>/', views.user_profile, name='userprofile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('view_publication/<int:post_id>/', views.view_publication, name='view_publication'),
    path('library/', views.library, name='library'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('add_publication/', views.add_publication, name='add_publication'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('like_post_ajax/<int:post_id>/', views.like_post_ajax, name='like_post_ajax'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
