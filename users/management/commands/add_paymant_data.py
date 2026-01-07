from django.core.management import BaseCommand, call_command

from config.settings import BASE_DIR


class Command(BaseCommand):
    help = "Custom command to add payment data"

    def handle(self, *args, **options) -> None:
        """
        Method to add payment data
        """

        call_command("loaddata", str(BASE_DIR / "fixtures" / "payment_fixtures.json"))

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
