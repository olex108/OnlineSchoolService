from gc import get_objects
from http.client import responses
from typing import Any
from drf_yasg import openapi

from django.utils.decorators import method_decorator
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
from .permissions import IsOwner, IsModer
from .serializers import (PaymentSerializer, UserRegisterSerializer, UserRetrieveSerializer, UserSerializer,
                          SubscriptionSerializer)

from drf_yasg.utils import swagger_auto_schema



class UserRegisterAPIView(generics.CreateAPIView):
    """
    Register new user. For any user
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


@method_decorator(name='get', decorator=swagger_auto_schema(responses={200: UserRetrieveSerializer()}))
class UserRetrieveAPIView(generics.RetrieveAPIView):
    """
    Get user by id. With fields "email", "first_name", "phone", "country", "avatar" for any authenticated user
    and extra "last_name", "payment_history" for owner user
    """

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


@method_decorator(
    name='get',
    decorator=swagger_auto_schema(responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                'message': openapi.Schema(type=openapi.TYPE_STRING, example="Верификация по email прошла успешно"),
            }
        )})
)
class UserEmailVerificationAPIView(APIView):
    """
    Class for verification of user email

    return: Response of status of verification
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
    """
    Get payments list with filters fields "paid_course", "paid_lesson", "payment_method",
    and ordering field "payment_date".
    For moderators users
    """

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated, IsModer]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("paid_course", "paid_lesson", "payment_method")
    ordering_fields = ("payment_date",)

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, example="Подписка добавлена"),
            }
        )})
)
class SubscribeAPIView(APIView):
    """
    Class for subscription user for courses.
    Get post request with data of course id in dict

    {"course_id": course_id: int}

    """

    def get(self, request: Any, pk: int) -> Response:
        """
        Post request with data of course id in dict {"course_id": course_id: int}.
        return: Response with message of subscription in form {"message": message: str} if course is exist
        or {"detail": "No Course matches the given query."} course isn`t exist
        """

        user = self.request.user
        course_id = pk
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
