from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class VGUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='none_avatar.png', verbose_name='Аватар')
    short_description = models.CharField(max_length=30, blank=True, null=True, verbose_name='Краткое описание')

class PostVGUser(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    likes = models.PositiveIntegerField(default=0, verbose_name='Кол-во лайков')
    image = models.ImageField(upload_to='content', blank=True, null=True, verbose_name='Фото')
    author = models.ForeignKey(VGUser, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')

    def clean(self):
        if not self.description and not self.image:
            raise ValidationError({
                'description': 'Необходимо предоставить либо описание, либо фото',
                'image': 'Необходимо предоставить либо описание, либо фото'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Chat(models.Model):
    chat_id = models.CharField(max_length=20, unique=True)
    user1 = models.ForeignKey(VGUser, on_delete=models.CASCADE, related_name='chats_initiated')
    user2 = models.ForeignKey(VGUser, on_delete=models.CASCADE, related_name='chats_received')
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('chat_id', 'user1', 'user2')

    def __str__(self):
        if self.user1 == self.user2:
            return f'Избранное'
        return f'Чат {self.user1} и {self.user2}'
    
    def update_activity(self):
        self.save()
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(VGUser, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)        
    is_read = models.BooleanField(default=False)


    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender}: {self.text[:20]}...'
