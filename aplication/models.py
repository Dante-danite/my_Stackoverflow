from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from users.models import User


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    date_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Основная часть')
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    views = models.IntegerField(default=0, verbose_name='Просмотры', blank=False)


    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['author']

    def __str__(self):
        return self.title

    def total_views(self):
        self.views += 1
        self.save()


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос', related_name='answers')
    text = models.TextField(verbose_name='Основная часть')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    date_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    status_accepted = models.BooleanField(default=False, verbose_name='Статус лучшего ответа')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['author']

    def __str__(self):
        return f'Ответ от {self.author.username} на {self.question.title} с содержанием {self.text}'


class FavoritQuestion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Главный')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Любимые вопросы'
        verbose_name_plural = 'Любимые вопросы'
        ordering = ['author']

    def __str__(self):
        return f'Пользователь {self.author.username} добавил вопрос {self.question.title}'


class FavoritAnswer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Главный ')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Любимые ответы'
        verbose_name_plural = 'Любимые ответы'
        ordering = ['author']

    def __str__(self):
        return f'Пользователь {self.author.username} добавил ответ {self.answer.text[:100]}...'


class VoiceQuestion(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Главный')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    status = models.BooleanField(null=True, default=False)

    class Meta:
        verbose_name = 'Голос за вопрос'
        verbose_name_plural = 'Голоса за вопросы'
        ordering = ['author']

    def __str__(self):
        return f'Пользователь {self.author.username} проголосовал за вопрос {self.question.title}'


class VoiceAnswer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Главный')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, verbose_name='Ответ')
    status = models.BooleanField(null=True, default=False)

    class Meta:
        verbose_name = 'Голос за ответ'
        verbose_name_plural = 'Голоса за ответы'
        ordering = ['author']

    def __str__(self):
        return f'Пользователь {self.author.username} проголосовал за ответ {self.answer.text}'


class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Вопрос', related_name='comments_question')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Ответ', related_name='comments_answer')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Основная часть')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата обновления')
    date_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['author']

    def __str__(self):
        return f'Пользователь {self.author.username} прокомментировал  {self.text}'
