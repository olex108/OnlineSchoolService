from rest_framework import serializers

from courses.models import Course, Lesson
from users.models import User


class PaymentServices:

    @classmethod
    def save_payment_obj(cls, serializer: serializers, owner: User) -> tuple[serializers, Course | Lesson]:
        """
        Method get serializer and user object
        get name and price of payd object, save Payment object

        return: saved serializer of Payment object
        return: name of payd object
        """

        paid_course = serializer.validated_data.get("paid_course")
        paid_lesson = serializer.validated_data.get("paid_lesson")
        print(paid_course, paid_lesson)

        try:
            if not paid_course and not paid_lesson:
                raise serializers.ValidationError("Заполните одно из полей 'paid_course' или 'paid_lesson'.")
            if paid_course:
                product_obj = paid_course
                amount = paid_course.price
            else:
                product_obj = paid_lesson
                amount = paid_lesson.price
            if not amount:
                raise serializers.ValidationError("Данный курс бесплатный")

        except Course.DoesNotExist or Lesson.DoesNotExist:
            raise serializers.ValidationError("Неверный номер курса")

        return serializer.save(amount=amount, owner=owner), product_obj
