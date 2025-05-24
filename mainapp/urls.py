from django.urls import path
from django.views.generic import TemplateView
from mainapp import views

urlpatterns = [
    path('search-users/', views.search_users_view, name='search_users'),
    path('user-page/<int:user_id>', views.user_personal_page, name='user_personal_page'),
    path('chat/<int:chat_id>', views.personal_chat_room_view, name='personal_chat_room'),
    path('my-chats/', views.my_chats, name='my_chats'),
]
