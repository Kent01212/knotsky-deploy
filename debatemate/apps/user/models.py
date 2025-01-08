import hashlib
import secrets
import hmac
import uuid

from django.db import models
from django.utils.timezone import now, timedelta
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser

from .settings import (
    USER_OTP_LENGTH,
    USER_OTP_CHARSET,
    USER_OTP_SALT_HEX_LENGTH,
    USER_OTP_HASH_HEX_LENGTH,
)

from .managers import UserManager


class User(AbstractBaseUser):

    """
    Account
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    email = models.EmailField(
        max_length=255,
        unique=True
    )

    icon = models.ImageField(
        upload_to='icon/',
        default='https://via.placeholder.com/256x256.png'
    )

    about = models.TextField(
        max_length=1024,
        default='',
        blank=True
    )

    is_active = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def is_staff(self) -> bool:
        return False

    @property
    def is_superuser(self) -> bool:
        return False


class UserOTP(models.Model):

    """
    One Time Password Token
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        editable=False,
        unique=True
    )

    token_hash = models.CharField(
        max_length=USER_OTP_HASH_HEX_LENGTH,
        default=secrets.token_hex(USER_OTP_HASH_HEX_LENGTH),
    )

    token_salt = models.CharField(
        max_length=USER_OTP_SALT_HEX_LENGTH,
        default=secrets.token_hex(USER_OTP_SALT_HEX_LENGTH),
    )

    expired_at = models.DateTimeField(
        default=now,
    )

    @property
    def is_expired(self) -> bool:
        """
        Check if One Time Password Token is expired
        """
        return now() > self.expired_at

    def check_token(self, token: str) -> bool:
        """
        Verify One Time Password Token
        """
        if self.is_expired or len(token) != 8:
            return False
        token_salt = bytes.fromhex(self.token_salt)
        token_hash = bytes.fromhex(self.token_hash)
        token_hash_x = hashlib.sha3_512(token_salt + token.encode('utf-8')).digest()
        if ok := hmac.compare_digest(token_hash, token_hash_x):
            self.expired_at = now()
            self.save()
        return ok

    def issue_token(self) -> str:
        """
        Issue OTP ([0-9A-Z]{8})
        """
        token = get_random_string(USER_OTP_LENGTH, USER_OTP_CHARSET)
        token_salt = secrets.token_bytes(USER_OTP_SALT_HEX_LENGTH)
        token_hash = hashlib.sha3_512(token_salt + token.encode('utf-8')).digest()
        self.token_salt = token_salt.hex()
        self.token_hash = token_hash.hex()
        self.expired_at = now() + timedelta(minutes=5)
        self.save()
        return token

    def issue_token_and_send(self, email: str):
        """
        Issue OTP and send to email
        """
        send_mail(
            'Debatemate OTP Authentication',
            f'Your OTP: {self.issue_token()}, Timeout: 5 minutes',
            'kd1358122@st.kobedenshi.ac.jp',
            [email],
        )
