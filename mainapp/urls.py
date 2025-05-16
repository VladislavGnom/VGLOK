from django.urls import path
from django.views.generic import TemplateView
from mainapp import views

urlpatterns = [
    path('search-users/', views.search_users_view, name='search_users'),
    path('user-page/<int:user_id>', views.user_personal_page, name='user_personal_page'),
    path('chat/<int:chat_room>', TemplateView.as_view(template_name='mainapp/chat_room.html'), name='chat_room'),
]
