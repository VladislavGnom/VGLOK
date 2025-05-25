from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from mainapp.models import Chat
from mainapp.utils import create_chat_between_current_and_new_user, is_chat_room_exist

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

    if '-' not in chat_id:
        received_user = get_object_or_404(User, pk=chat_id)
    else:
        user_ids = chat_id.split('-')
        received_user_id = list(filter(lambda pk: int(pk) != user.pk, user_ids))

        if not received_user_id and user_ids.count(str(user.pk)) == 2:
            received_user_id = user.pk    # избранное
        else:
            received_user_id = received_user_id[0]

        received_user = get_object_or_404(User, pk=received_user_id)

    if user.username == received_user.username:
        title = 'Избранное'
    else:
        title = f'Чат {user.username} и {received_user.username}'

    # if chat has already exist
    if is_chat_room_exist(chat_id=chat_id):
        return render(request, 'mainapp/chat_room.html', context={'title': title, 'chat_id': chat_id})

    # otherwise chat_id is the pk of the receiving user
    chat_id = create_chat_between_current_and_new_user(request=request, received_user=received_user)   
    if not chat_id: return 

    context = {
        'title': title,
        'chat_id': chat_id, 
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
