# seed_users.py
from django.apps import AppConfig
from django.core.management.base import BaseCommand
from debatemate.apps.user.models import User
from faker import Faker


class Command(BaseCommand):

    def handle(self, *args, **options):

        # 　既存のアカウントを削除
        User.objects.all().delete()

        # アカウントをループで作成
        for dummyuser in [
            {'name': 'user1', 'email': 'user1@test.com', 'password': 'password1'},
            {'name': 'user2', 'email': 'user2@test.com', 'password': 'password2'},
            {'name': 'user3', 'email': 'user3@test.com', 'password': 'password3'},
            {'name': 'user4', 'email': 'user4@test.com', 'password': 'password4'},
            {'name': 'user5', 'email': 'user5@test.com', 'password': 'password5'},
            {'name': 'user6', 'email': 'user6@test.com', 'password': 'password6'},
            {'name': 'user7', 'email': 'user7@test.com', 'password': 'password7'},
            {'name': 'user8', 'email': 'user8@test.com', 'password': 'password8'},
            {'name': 'user9', 'email': 'user9@test.com', 'password': 'password9'},
        ]:
            # アカウント作成成功アナウンス
            user = User.objects.create_user(**dummyuser)
            user.is_active = True
            user.save()

            # アカウント作成成功アナウンス
            self.stdout.write(self.style.SUCCESS('アカウント作成に成功しました！'))

        # 全てのアカウント作成作成アナウンス
        self.stdout.write(self.style.SUCCESS('全てのアカウント作成に成功しました！'))
