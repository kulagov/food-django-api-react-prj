from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(
        max_length=30,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия')
    email = models.EmailField('Электронная почта')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='follower',
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='follow',
        verbose_name='Подписка'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),
        )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} -> {self.following}'
