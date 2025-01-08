from django.core.management.base import BaseCommand
from debatemate.apps.bot.models import Bot
from debatemate.apps.user.models import User


class Command(BaseCommand):
    help = 'Seed the Bot model with test data'

    def handle(self, *args, **kwargs):

        # Create a Faker instance
        user = User.objects.first()

        # Delete existing data
        Bot.objects.all().delete()

        # Check if the Bot model is empty
        for dummybot in [
            {'name': 'bot1', 'owner': user},
            {'name': 'bot2', 'owner': user},
            {'name': 'bot3', 'owner': user},
            {'name': 'bot4', 'owner': user},
            {'name': 'bot5', 'owner': user},
        ]:
            # Create dummy bot
            bot = Bot.objects.create(**dummybot)

        # Console output
        self.stdout.write(self.style.SUCCESS('Deleted old bot data'))
