from django.shortcuts import render, get_object_or_404, redirect, resolve_url, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpRequest, HttpResponseRedirect

from mainapp.models import Chat, PostVGUser, Like
from mainapp.utils import create_chat_between_current_and_new_user, is_chat_room_exist
from mainapp.forms import PostVGUserForm, CommentForm

User = get_user_model() 

@login_required
def search_users_view(request: HttpRequest) -> HttpResponse:
    user = request.user
    all_loged_users = User.objects.exclude(username=user.username)

    context = {
        'title': 'Поиск пользователей',
        'all_loged_users': all_loged_users,
    }

    return render(request, 'mainapp/search_users_page.html', context=context)

@login_required
def user_personal_page(request: HttpRequest, user_id: int) -> HttpResponse:
    target_user = get_object_or_404(User, pk=user_id)
    title_page = 'Моя страница' if request.user.pk == user_id else f'Страница - {target_user.username}'

    posts = target_user.posts.all().order_by('-created_at')
    
    for post in posts:
        post._request = request
    
    comment_form = CommentForm()

    context = {
        'title': title_page,
        'user': target_user,
        'posts': posts,
        'comment_form': comment_form,
    }

    return render(request, 'mainapp/user_personal_page.html', context=context)

@login_required
def personal_chat_room_view(request: HttpRequest, chat_id: str) -> HttpResponse:
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
def my_chats(request: HttpRequest) -> HttpResponse:
    user = request.user 

    context = {
        'title': 'Мои чаты',
        'my_chats': Chat.objects.filter(Q(user1=user) | Q(user2=user))
    }

    return render(request, 'mainapp/my_chats.html', context=context)

@login_required
def create_new_post_view(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    user = request.user

    if request.method == "POST":
        form = PostVGUserForm(request.POST, request.FILES)

        if form.is_valid():
            user_post = form.save(commit=False)
            user_post.author = request.user
            user_post.save()

            redirected_url = resolve_url('user_personal_page', user.pk)
            return redirect(redirected_url)
    else:
        form = PostVGUserForm()

    context = {
        'title': 'Создание поста',
        'form': form,
    }

    return render(request, 'mainapp/create_post.html', context=context)

def update_exist_post_view(requset: HttpRequest):
    ...

@login_required
def handle_comment(request: HttpRequest) -> HttpResponse | HttpResponseBadRequest:
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user

            post_pk = request.POST.get('post-pk')
            post = PostVGUser.objects.get(pk=post_pk)

            comment.post = post
            comment.save()

        return HttpResponse(f"""
            <li>{ comment.author.username }: { comment.text }</li>
        """)

    return HttpResponseBadRequest()    # GET and other methods are not support for this action

@login_required
def toggle_like(request: HttpRequest, post_id: int) -> HttpResponse | HttpResponseBadRequest:
    if request.method == 'POST':
        post = get_object_or_404(PostVGUser, id=post_id)
        user = request.user
        like, created = Like.objects.get_or_create(post=post, author=user)
        
        if not created:
            like.delete()
            heart_svg = render_to_string('icons/heart-unliked.svg')
        else:
            heart_svg = render_to_string('icons/heart-liked.svg')

        return HttpResponse(f"""
            <span>{post.like_count()}</span>
            <span class="heart">{heart_svg}</span>
        """)
    
    return HttpResponseBadRequest()    # GET and other methods are not support for this action
