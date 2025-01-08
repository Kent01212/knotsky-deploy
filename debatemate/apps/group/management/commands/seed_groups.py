# seed_groups.py
from django.core.management.base import BaseCommand

from debatemate.apps.group.models import (
    Group,
    GroupUser
)

from debatemate.apps.user.models import User


class Command(BaseCommand):

    help = 'Seed groups'

    def handle(self, *args, **options):

        # Account seeder programs.
        user = User.objects.first()

        # Group seeder programs.
        Group.objects.all().delete()

        for dummygroup in [
            {'name': 'Group Test-1', 'owner': user},
        ]:
            # Create dummy group.
            group = Group.objects.create(**dummygroup)

            # Group seeder programs.
            self.stdout.write(self.style.SUCCESS(f'グループの作成に成功：UUID={group.id}'))

        # GroupUser seeder programs.
        self.stdout.write(self.style.SUCCESS('全てのグループ作成に成功しました！'))
