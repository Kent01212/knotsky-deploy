from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    """
    User Manager
    """

    def create_user(self, name: str, email: str, password: str):
        """
        Create User
        """
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
