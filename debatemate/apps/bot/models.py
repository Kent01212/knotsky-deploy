from django.db import models


class Bot(models.Model):

    owner = models.ForeignKey(
        to='user.User',
        on_delete=models.CASCADE,
        related_name='bots'
    )

    name = models.CharField(
        max_length=255
    )

    icon = models.ImageField(
        upload_to='icon/',
        default='https://via.placeholder.com/256'
    )

    description = models.TextField(
        max_length=1024,
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )
