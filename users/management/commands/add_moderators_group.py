from django.contrib.auth.models import Group, Permission

from django.core.management import BaseCommand

from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):
    help = " Add moderators group"

    def handle(self, *args, **options):
        """Check if group is exist, and add Moderators group, add permissions"""

        try:
            group = Group.objects.get(name="Модераторы")
            print(f"Группа {group.name} уже существует")
        except ObjectDoesNotExist:
            moderators_group = Group.objects.create(name="Модераторы")
            moderators_group.save()
            # Add permissions

            self.stdout.write(self.style.SUCCESS(f"Группа {moderators_group.name} успешно создана"))
