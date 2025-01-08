import uuid

from django.db import models


class Debate(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    group = models.ForeignKey(
        to='group.Group',
        on_delete=models.CASCADE,
        editable=False
    )

    title = models.CharField(
        max_length=255
    )

    description = models.TextField(
        max_length=1024,
        blank=True,
        default="",
    )


class DebateUser(models.Model):

    user = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        editable=False
    )

    debate = models.ForeignKey(
        to=Debate,
        on_delete=models.CASCADE,
        editable=False
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=['user', 'debate'],
                name='unique_user_debate'
            )
        ]


class DebateMessage(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    author = models.ForeignKey(
        to=DebateUser,
        on_delete=models.CASCADE,
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
