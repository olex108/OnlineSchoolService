from rest_framework.serializers import ValidationError


VALID_LINKS = ("https://www.youtube.com/", "https://www.youtu.be/", "https://youtube.com/", "https://youtu.be/",
               "youtube.com/", "youtu.be/")


class VideoUrlValidator:
    def __init__(self, field: str) -> None:
        self.field = field

    def __call__(self, value: dict) -> None:

        url = value.get(self.field)

        if not url.startswith(VALID_LINKS):
            raise ValidationError("Ссылка должна быть на сайт https://www.youtube.com/...")
