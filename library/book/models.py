import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Book(models.Model):
    title = models.CharField(
        max_length=255, verbose_name='Название', unique=True
    )
    description = models.TextField(verbose_name='Описание')
    publication_date = models.DateField(
        default=datetime.datetime.now, verbose_name='Дата'
    )
    author = models.ForeignKey(
        'Author', on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'книгу'
        verbose_name_plural = 'Книги'


class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='пользователь',
        primary_key=True,
        blank=True,
    )
    first_name = models.CharField(
        max_length=255, verbose_name='Имя', null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, verbose_name='Фамилия', null=True, blank=True
    )
    birthday = models.DateField(
        default=datetime.datetime.now,
        verbose_name='День рождения',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.user.username}'

    def __repr__(self):
        return f'{self.__dict__}'

    @receiver(post_save, sender=User)
    def create_author(sender, instance, created, **kwargs):
        if created:
            Author.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_author(sender, instance, **kwargs):
        instance.author.save()

    class Meta:
        verbose_name = 'автора'
        verbose_name_plural = 'Авторы'
