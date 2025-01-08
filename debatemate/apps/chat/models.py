import uuid

from django.db import models


class Chat(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    group = models.ForeignKey(
        to='group.Group',
        on_delete=models.CASCADE,
        editable=False
    )

    name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        max_length=1024,
        default="",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=['name', 'group'],
                name='unique_name_group'
            )
        ]


class ChatMessage(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        editable=False
    )

    author = models.ForeignKey(
        to='group.GroupUser',
        on_delete=models.PROTECT,
        editable=False
    )

    content = models.TextField(
        max_length=1024,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
