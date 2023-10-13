from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'letter_app'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('conversation/<str:contact_username>/', views.conversation, name='conversation'),
    path('send_message/<str:contact_username>/', views.send_message, name='send_message'),
    path('accept_friend_request/<int:contact_id>/', views.accept_friend_request, name='accept_friend_request'),


    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('group_chat/<int:group_id>/', views.group_chat, name='group_chat'),
    path('group/<int:group_id>/send_message/', views.send_group_message, name='send_group_message'),
    path('groups/create/', views.create_group, name='create_group'),
    path('group/add_member/<int:group_id>/', views.add_contacts_to_group, name='add_contacts_to_group'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('group/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('group/promote_member/<int:group_id>/<int:member_id>/', views.promote_member, name='promote_member'),
    path('group/remove_member/<int:group_id>/<int:member_id>/', views.remove_member, name='remove_member'),
    path('group/remove_admin/<int:group_id>/<int:member_id>/', views.remove_admin, name='remove_admin'),
    path('group/leave_group/<int:group_id>/', views.leave_group, name='leave_group'),
    path('group/delete_group/<int:group_id>/', views.delete_group, name='delete_group'),

    path('join_group/<str:unique_code>/', views.join_group, name='join_group'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
