from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from mainapp.models import PostVGUser

User = get_user_model()

def search_users_view(request):
    all_loged_users = User.objects.all()

    context = {
        'title': 'Поиск пользователей',
        'all_loged_users': all_loged_users,
    }

    return render(request, 'mainapp/search_users_page.html', context=context)

def user_personal_page(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    title_page = 'Моя страница' if request.user.pk == user_id else f'Страница - {target_user.username}'

    posts = target_user.posts.all()

    context = {
        'title': title_page,
        'user': target_user,
        'posts': posts
    }

    return render(request, 'mainapp/user_personal_page.html', context=context)
