from django.urls import path
from mainapp import views

urlpatterns = [
    path('search-users/', views.search_users_view, name='search_users'),
    path('user-page/<int:user_id>', views.user_personal_page, name='user_personal_page'),
]
