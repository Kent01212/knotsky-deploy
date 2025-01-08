from django.core.management.base import BaseCommand

from debatemate.apps.user.models import (
    User
)

from debatemate.apps.group.models import (
    Group,
    GroupUser
)

from debatemate.apps.chat.models import (
    Chat,
    ChatMessage
)


class Command(BaseCommand):

    help = 'Seeds the database with all necessary initial data'

    def handle(self, *args, **options):

        # Delete existing data.
        Chat.objects.all().delete()

        # Get group.
        group = Group.objects.first()

        # Group seeder programs.
        for dummychat in [
            {'group': group, 'name': 'Chat Test-1'},
            {'group': group, 'name': 'Chat Test-2'},
            {'group': group, 'name': 'Chat Test-3'},
            {'group': group, 'name': 'Chat Test-4'},
            {'group': group, 'name': 'Chat Test-5'},
            {'group': group, 'name': 'Chat Test-6'},
        ]:
            # Group seeder programs.
            chat = Chat.objects.create(**dummychat)

            # Console output.
            self.stdout.write(self.style.SUCCESS(f'チャットの作成に成功：UUID={chat.id}'))

        # Console output.
        self.stdout.write(self.style.SUCCESS('チャットのダミーデータの作成に成功しました！'))

        # Get user.
        user = User.objects.first()

        # Group seeder programs.
        group_user = GroupUser.objects.create(group=group, user=user)

        for dummymessage in [
            {'chat': chat, 'author': group_user, 'content': 'Message Test-1'},
            {'chat': chat, 'author': group_user, 'content': 'Message Test-2'},
            {'chat': chat, 'author': group_user, 'content': 'Message Test-3'},
            {'chat': chat, 'author': group_user, 'content': 'Message Test-4'},
            {'chat': chat, 'author': group_user, 'content': 'Message Test-5'},
            {'chat': chat, 'author': group_user, 'content': 'Message Test-6'},
        ]:
            # Group seeder programs.
            message = ChatMessage.objects.create(**dummymessage)

            # Console output.
            self.stdout.write(self.style.SUCCESS(
                f'メッセージの作成に成功：UUID={message.id}'))

        # Console output.
        self.stdout.write(self.style.SUCCESS('Successfully seeded data'))
