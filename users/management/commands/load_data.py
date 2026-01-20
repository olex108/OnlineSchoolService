import json

from django.core.management import BaseCommand, call_command

from config.settings import BASE_DIR
from courses.models import Course, Lesson
from users.models import User


class Command(BaseCommand):
    help = "Loads data from JSON data_fixtures"

    def handle(self, *args, **options) -> None:
        """
        Method to load data from JSON data_fixtures

        Get list of pk of users from JSON data_fixtures file, del users with pk from list
        Add users from JSON data_fixtures file
        Load courses and lessons data from JSON data_fixtures files
        """

        # Get users from data_fixtures
        path_to_file = BASE_DIR / "data_fixtures" / "users_fixtures.json"
        with open(path_to_file) as json_file:
            users_data = json.load(json_file)

        # Delete users with pk from data_fixtures
        users_pk_list = [user["pk"] for user in users_data]
        for pk in users_pk_list:
            try:
                User.objects.get(pk=pk).delete()
            except Exception as e:
                print(e)

        # Add users from data_fixtures
        for user in users_data:
            new_user = User.objects.create(
                id=user["pk"],
                email=user["fields"]["email"],
                first_name=user["fields"]["first_name"],
                is_active=user["fields"]["is_active"],
            )
            new_user.set_password(user["fields"]["password"])
            new_user.save()

        User.objects.get(pk=1).delete()
        super_user = User.objects.create(
            id=1,
            email="admin@test.com",
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        super_user.set_password("1234qwer")
        super_user.save()

        # Delete and add objects Courses, Lesson, Payment
        Course.objects.all().delete()
        Lesson.objects.all().delete()

        call_command("loaddata", str(BASE_DIR / "data_fixtures" / "courses_fixtures.json"))
        call_command("loaddata", str(BASE_DIR / "data_fixtures" / "lessons_fixtures.json"))

        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
