import secrets
import uuid

from django.utils.timezone import now, timedelta
from django.db import models


class HS256(models.Model):

    """
    HS256 Secret-key Manager
    """

    # Secret-key UUID.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Secret-key of HS256 Algorithm.
    secret_key = models.BinaryField(max_length=32, editable=False)

    # Datetime of HS256 Secret-key created at.
    created_at = models.DateTimeField(editable=False)

    # Datetime of HS256 Secret-key expired at.
    expired_at = models.DateTimeField(editable=False)

    @classmethod
    def new(cls):
        """
        HMAC鍵を生成する
        """
        self = HS256()
        self.secret_key = secrets.token_bytes(32)
        self.created_at = now()
        self.expired_at = self.created_at + timedelta(days=30)
        self.save()
        return self

    @property
    def is_valid(self):
        """
        HMAC鍵の有効性を検証する
        """
        return self.created_at < now() < self.expired_at
