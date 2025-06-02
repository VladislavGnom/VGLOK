from django.urls import path
from django.views.generic import TemplateView
from mainapp import views

urlpatterns = [
    path('search-users/', views.search_users_view, name='search_users'),
    path('user-page/<int:user_id>', views.user_personal_page, name='user_personal_page'),
    path('chat/<slug:chat_id>', views.personal_chat_room_view, name='personal_chat_room'),
    path('my-chats/', views.my_chats, name='my_chats'),
    path('create-post/', views.create_new_post_view, name='create_post'),
    path('update-post/<int:post_id>', views.update_exist_post_view, name='update_post'),
    path('delete-post/<int:post_id>', views.delete_exist_post_view, name='delete_post'),
    path('commit-comment/', views.handle_comment, name='handle_comment'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),
]
