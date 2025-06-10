from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class VGUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='none_avatar.png', verbose_name='Аватар')
    short_description = models.CharField(max_length=30, blank=True, null=True, verbose_name='Краткое описание')


class PostVGUser(models.Model):
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='content', verbose_name='Фото', blank=True)
    author = models.ForeignKey(VGUser, on_delete=models.CASCADE, related_name='posts', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()
    

    def clean(self):
        if not self.image and not self.description:
            raise ValidationError({
                'description': 'Необходимо предоставить либо описание, либо фото',
                'image': 'Необходимо предоставить либо описание, либо фото'
            })
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_liked_by_current_user(self):
        from django.core.exceptions import AppRegistryNotReady
        try:
            return self.likes.filter(author=self._request.user).exists()
        except (AttributeError, AppRegistryNotReady):
            return False


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
    

class Comment(models.Model):
    post = models.ForeignKey(PostVGUser,on_delete=models.CASCADE, related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(VGUser, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Содержимое комментария')
    timestamp = models.DateTimeField(auto_now_add=True)        

    def clean(self):
        if not self.text:
            raise ValidationError({
                'text': 'Необходимо заполнить это поле',
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'Комментарий: {self.text[:20]}...'
    

class Like(models.Model):
    post = models.ForeignKey(PostVGUser,on_delete=models.CASCADE, related_name='likes', verbose_name='Пост')
    author = models.ForeignKey(VGUser, on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together = ['post', 'author'] 

    def __str__(self):
        return f'Лайк - {self.author.username}'
    