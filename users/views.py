from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Payment
from .serializers import UserRegisterSerializer, UserSerializer, UserRetrieveSerializer, PaymentSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserEmailVerificationAPIView(APIView):
    """
    Class for verification of user email

    :return: Response of status of verification
    """

    def get(self, request, token: str) -> Response:
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
    filterset_fields = ('paid_course', 'paid_lesson', "payment_method")
    ordering_fields = ("payment_date",)
