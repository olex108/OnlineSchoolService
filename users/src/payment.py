from users.models import Payment, Transfer

from users.models import User
from courses.models import Course, Lesson

from rest_framework import serializers

from users.src.transfer_api_service import StripeAPIService
from config.settings import STRIPE_API_KEY


class PaymentServices:


    @classmethod
    def save_payment_obj(cls, serializer: serializers, user: User) -> tuple[serializers, str]:
        """
        Method get serializer and user object
        get name and price of payd object, save Payment object

        return: saved serializer of Payment object
        return: name of payd object
        """

        paid_course = serializer.validated_data.get("paid_course")
        paid_lesson = serializer.validated_data.get("paid_lesson")

        try:
            if paid_course:
                product_name = paid_course.name
                amount = paid_course.price
            else:
                product_name = paid_lesson.name
                amount = paid_lesson.price
            if not amount:
                raise serializers.ValidationError("Данный курс бесплатный")

        except Course.DoesNotExist or Course.DoesNotExist:
            raise serializers.ValidationError("Неверный номер курса")

        return serializer.save(
            amount=amount,
            user=user
        ), product_name
