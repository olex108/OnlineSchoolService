import json

from django.core.management import BaseCommand, call_command

from config.settings import BASE_DIR
from courses.models import Course, Lesson
from users.models import User


class Command(BaseCommand):
    help = "Loads data from JSON fixtures"

    def handle(self, *args, **options) -> None:
        """
        Method to load data from JSON fixtures

        Get list of pk of users from JSON fixtures file, del users with pk from list
        Add users from JSON fixtures file
        Load courses and lessons data from JSON fixtures files
        """

        # Get users from fixtures
        path_to_file = BASE_DIR / "fixtures" / "users_fixtures.json"
        with open(path_to_file) as json_file:
            users_data = json.load(json_file)

        # Delete users with pk from fixtures
        users_pk_list = [user["pk"] for user in users_data]
        for pk in users_pk_list:
            try:
                User.objects.get(pk=pk).delete()
            except Exception as e:
                print(e)

        # Add users from fixtures
        for user in users_data:
            new_user = User.objects.create(
                id=user["pk"],
                email=user["fields"]["email"],
                first_name=user["fields"]["first_name"],
                is_active=user["fields"]["is_active"],
            )
            new_user.set_password(user["fields"]["password"])
            new_user.save()

        # Delete and add objects Courses, Lesson, Payment
        Course.objects.all().delete()
        Lesson.objects.all().delete()

        call_command("loaddata", str(BASE_DIR / "fixtures" / "courses_fixtures.json"))
        call_command("loaddata", str(BASE_DIR / "fixtures" / "lessons_fixtures.json"))

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
