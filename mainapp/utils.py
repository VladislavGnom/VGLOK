from django.db import IntegrityError
from django.http import HttpRequest

from mainapp.models import Chat, VGUser

def create_chat_id(user_id_1: int, user_id_2: int) -> str:
    chat_id = map(str, sorted([user_id_1, user_id_2]))
    return '-'.join(chat_id)

def is_chat_room_exist(chat_id):
    try:
        Chat.objects.get(chat_id=chat_id)
        return True
    except:  
        return False
    
def create_chat_between_current_and_new_user(request: HttpRequest, received_user: VGUser) -> bool | str:
    user = request.user
    chat_id = create_chat_id(user_id_1=user.pk, user_id_2=received_user.pk)

    try:
        Chat.objects.create(
            chat_id=chat_id,
            user1=request.user,
            user2=received_user,
        )
        return chat_id
    except IntegrityError:    # object is already exist
        return chat_id
    except Exception:
        return False  
    