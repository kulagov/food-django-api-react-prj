from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=150)
    email = models.EmailField('email address')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='follower',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='follow',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_follow'
            ),
        )

    def __str__(self):
        return f'{self.user} -> {self.following}'
