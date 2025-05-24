from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from mainapp.models import PostVGUser, Chat
from mainapp.utils import unificate_chat_id

User = get_user_model()

@login_required
def search_users_view(request):
    all_loged_users = User.objects.all()

    context = {
        'title': 'Поиск пользователей',
        'all_loged_users': all_loged_users,
    }

    return render(request, 'mainapp/search_users_page.html', context=context)

@login_required
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

@login_required
def personal_chat_room_view(request, chat_id):
    user = request.user

    # if chat has already exist
    try:
        Chat.objects.get(chat_id=chat_id)
        return render(request, 'mainapp/chat_room.html', context={'chat_id': chat_id})
    except:  
        ...

    # otherwise chat_id is the pk of the recepient user
    unificated_chat_id = unificate_chat_id(chat_id_1=chat_id, chat_id_2=user.pk)
    received_user = get_object_or_404(User, pk=chat_id)

    try:
        Chat.objects.create(
            chat_id=unificated_chat_id,
            user1=request.user,
            user2=received_user,
        )
    except:
        ...    

    context = {
        'chat_id': unificated_chat_id, 
    }

    return render(request, 'mainapp/chat_room.html', context=context)

@login_required
def my_chats(request):
    user = request.user 

    context = {
        'title': 'Мои чаты',
        'my_chats': Chat.objects.filter(Q(user1=user) | Q(user2=user))
    }

    return render(request, 'mainapp/my_chats.html', context=context)
