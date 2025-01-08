import uuid

from django.db import models


class Group(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    owner = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        blank=False
    )

    icon = models.ImageField(
        upload_to='group/icon/',
        default='https://placehold.com/256x256.png'
    )

    description = models.TextField(
        max_length=1024,
        blank=True,
        default='',
    )


class GroupUser(models.Model):

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        editable=False
    )

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        editable=False
    )

    nickname = models.CharField(
        max_length=255,
        blank=False
    )

    is_banned = models.BooleanField(
        default=False
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=['group', 'user'],
                name='unique_group_user'
            )
        ]


class GroupBot(models.Model):

    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        editable=False
    )

    bot = models.ForeignKey(
        to='bot.Bot',
        on_delete=models.CASCADE,
        editable=False
    )

    nickname = models.CharField(
        max_length=255,
        blank=False
    )

    is_banned = models.BooleanField(
        default=False
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=['group', 'bot'],
                name='unique_group_bot'
            )
        ]
