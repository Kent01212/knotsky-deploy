# seed_debates.py

from django.core.management.base import BaseCommand
from django.db import transaction
from debatemate.apps.user.models import User
from debatemate.apps.bot.models import Bot
from debatemate.apps.group.models import Group
from debatemate.apps.debate.models import Debate, DebateUser, DebateMessage
from faker import Faker

class Command(BaseCommand):
    help = 'Seeds the database with debates and related data using existing accounts and groups'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        fake = Faker('ja_JP')  # 日本語のダミーデータを生成
        
        self.stdout.write('Starting database seeding...')

        # 既存のアカウントを取得
        accounts = list(User.objects.all())
        if not accounts:
            self.stdout.write(
                self.style.ERROR('アカウントが見つかりません。python manage.py seed_accounts を先に実行してください。')
            )
            return

        # 既存のグループを取得
        groups = list(Group.objects.all())
        if not groups:
            self.stdout.write(
                self.style.ERROR('グループが見つかりません。python manage.py seed_groups を先に実行してください。')
            )
            return

        self.stdout.write(f'アカウント {len(accounts)}件、グループ {len(groups)}件 を確認')

        # 既存のデータを削除（オプション）
        Debate.objects.all().delete()
        DebateUser.objects.all().delete()
        DebateMessage.objects.all().delete()
        Bot.objects.all().delete()

        # Botの作成
        self.stdout.write('Botを作成中...')
        bots = []
        for i in range(5):
            bot = Bot.objects.create(
                name=f"Bot-{i+1}",
                icon='https://via.placeholder.com/256',
                description=fake.text(max_nb_chars=200),
                owner=fake.random_element(accounts)
            )
            bots.append(bot)
            self.stdout.write(f'  Bot作成成功: {bot.name}')

        # デベートの作成
        self.stdout.write('デベートを作成中...')
        debate_topics = [
            "環境問題について",
            "教育制度の改革",
            "働き方改革",
            "テクノロジーの進歩",
            "社会保障制度"
        ]

        for topic in debate_topics:
            # デベート作成
            debate = Debate.objects.create(
                title=topic,
                description=fake.text(max_nb_chars=200),
                group=fake.random_element(groups)
            )

            # デベート参加者の作成
            for account in accounts:
                DebateUser.objects.create(
                    user=account,
                    debate=debate
                )

            # デベートメッセージの作成
            debate_accounts = list(DebateUser.objects.filter(debate=debate))
            for _ in range(5):
                DebateMessage.objects.create(
                    content=fake.text(max_nb_chars=200),
                    author=fake.random_element(debate_accounts)
                )
            
            self.stdout.write(f'  デベート作成成功: {debate.title}')

        # 作成したデータの統計を表示
        self.stdout.write(
            self.style.SUCCESS(
                f'\nデータ作成完了!\n'
                f'作成されたデータ:\n'
                f'- 既存アカウント利用: {len(accounts)}件\n'
                f'- 既存グループ利用: {len(groups)}件\n'
                f'- Bot作成: {Bot.objects.count()}件\n'
                f'- デベート作成: {Debate.objects.count()}件\n'
                f'- デベート参加者: {DebateUser.objects.count()}件\n'
                f'- デベートメッセージ: {DebateMessage.objects.count()}件'
            )
        )