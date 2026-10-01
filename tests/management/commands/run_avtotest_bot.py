from django.core.management.base import BaseCommand
from avtotest_bot.main import main

class Command(BaseCommand):
    help = "AvtoTest Telegram Bot (@AvtoTestUzbBot) ni ishga tushirish"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("AvtoTest Telegram Bot ishga tushirilmoqda..."))
        try:
            main()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Bot to'xtatildi."))
