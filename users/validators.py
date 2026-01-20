from rest_framework.serializers import ValidationError


class PaymentValidator:
    def __init__(self, paid_course: str, paid_lesson: str) -> None:

        self.paid_course = paid_course
        self.paid_lesson = paid_lesson

    def __call__(self, value: dict) -> None:

        if value[self.paid_course] is None and value[self.paid_lesson] is None:
            raise ValidationError("Заполните одно из полей 'paid_course' или 'paid_lesson'.")
