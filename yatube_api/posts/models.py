from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Класс Group представляет собой группу, к которой можно присваивать посты.
# Содержит название группы (title), уникальный идентификатор (slug) и описание (description).
class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

# Класс Post представляет собой пост, создаваемый пользователем.
# Пост содержит текст (text), дату публикации (pub_date), автора (author),
# изображение (image) и опциональную привязку к группе (group).
class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='posts',
        null=True, blank=True)

    def __str__(self):
        return self.text

# Класс Comment представляет собой комментарий к посту.
# Каждый комментарий связан с пользователем (author) и постом (post),
# содержит текст (text) и дату добавления (created).
class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

# Класс Follow представляет собой подписку одного пользователя на другого.
# Связывает двух пользователей: user (тот, кто подписывается) и following (тот, на кого подписываются).
class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following')
