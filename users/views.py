from gc import get_objects
from http.client import responses
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from pyexpat.errors import messages
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment, User, Subscription
from courses.models import Course
from .permissions import IsOwner
from .serializers import (PaymentSerializer, UserRegisterSerializer, UserRetrieveSerializer, UserSerializer,
                          SubscriptionSerializer)


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return UserRetrieveSerializer
        else:
            return UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserEmailVerificationAPIView(APIView):
    """
    Class for verification of user email

    :return: Response of status of verification
    """

    permission_classes = [AllowAny]

    def get(self, request: Any, token: str) -> Response:
        try:
            user = User.objects.get(token=token)
            user.is_active = True
            user.save()

            return Response({"status": "success", "message": "Верификация по email прошла успешно"})
        except Exception as e:
            return Response({"status": "fail", "message": str(e)})


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)


class SubscribeAPIView(APIView):
    """
    Class for subscription user for courses.
    Get post request with data of course id in dict

    {"course_id": course_id: int}

    """

    def post(self, *args, **kwargs) -> Response:
        """
        Post request with data of course id in dict

        :return: Response with message of subscription in form {"message": message: str} if course is exist and
        {"detail": "No Course matches the given query."} course isn`t exist
        """

        user = self.request.user
        course_id = self.request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)
        try:
            subscription = Subscription.objects.get(user=user, course=course)
            if subscription.subscription:
                message = "Подписка удалена"
            else:
                message = "Подписка добавлена"
            subscription.subscription = not subscription.subscription
            subscription.save()
        except Subscription.DoesNotExist:
            Subscription.objects.create(user=user, course=course, subscription=True)
            message = "Подписка добавлена"

        return Response({"message": message})
