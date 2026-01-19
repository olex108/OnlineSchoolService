import logging

from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from config.settings import STRIPE_API_KEY
from courses.models import Course

from .models import Payment, Subscription, Transfer, User
from .permissions import IsModer, IsOwner
from .serializers import PaymentSerializer, UserRegisterSerializer, UserRetrieveSerializer, UserSerializer
from .src.payment import PaymentServices
from .src.transfer_api_service import StripeAPIService

logger = logging.getLogger("users")
payment_logger = logging.getLogger("payment")


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logger.info(f"Method: {request.method} - url: {request.path} - User: {request.data['email']}")
        return super().post(request, args, kwargs)


class UserRegisterAPIView(generics.CreateAPIView):
    """
    Register new user. For any user
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logger.info(f"Method: {request.method} - url: {request.path} - Registration of user: {request.data['email']}")
        return super().post(request, *args, **kwargs)


@method_decorator(name="get", decorator=swagger_auto_schema(responses={200: UserRetrieveSerializer()}))
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

    def put(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logger.info(f"Method: {request.method} - url: {request.path} - User: {request.data['email']}")
        return super().put(request, *args, **kwargs)


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        logger.info(f"Method: {request.method} - url: {request.path} - User: {request.data['email']}")
        return super().destroy(request, *args, **kwargs)


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Верификация по email прошла успешно"),
                },
            )
        }
    ),
)
class UserEmailVerificationAPIView(APIView):
    """
    Class for verification of user email

    return: Response of status of verification
    """

    permission_classes = [AllowAny]

    def get(self, request: Request, token: str) -> Response:
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


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsModer | IsOwner]

    def get_object(self):
        """
        Call method update_status of payment model for object
        """

        obj = super().get_object()
        obj.update_status()
        return obj


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer: PaymentSerializer) -> None:
        """
        Method for creating a new payment
        Call method PaymentServices.save_payment_obj for creating a new payment
        If payment method of payment "TRANSFER" create Transfer object
        """

        saved_payment_obj, product_obj = PaymentServices.save_payment_obj(serializer, owner=self.request.user)

        payment_logger.info(
            f"Create payment - Product: {product_obj.pk} {product_obj.name} - {saved_payment_obj.payment_method}"
        )

        if saved_payment_obj.payment_method == "TRANSFER":
            try:
                transfer_service = StripeAPIService(api_key=STRIPE_API_KEY)
                transfer_data = transfer_service.create_transfer_and_return_data(
                    product=product_obj, amount=saved_payment_obj.amount
                )
                Transfer.objects.create(
                    payment=Payment.objects.get(id=saved_payment_obj.id),
                    link=transfer_data.get("link"),
                    session_id=transfer_data.get("session_id"),
                    price_id=transfer_data.get("price_id"),
                    product_id=transfer_data.get("product_id"),
                )

                payment_logger.info(f"Create transfer - Transfer: {product_obj.pk} {product_obj.name}")

            except Exception as e:
                payment_logger.error(f"Create transfer error: {e} - Transfer: {product_obj.pk} {product_obj.name}")


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Подписка добавлена"),
                },
            )
        }
    ),
)
class SubscribeAPIView(APIView):
    """
    Class for subscription user for courses.
    Get post request with data of course id in dict

    {"course_id": course_id: int}
    """

    def get(self, request: Request, pk: int) -> Response:
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
            logger.info(f"Url: {request.path} - Subscription of user: {user.email} - course: {course.name}")
        except Subscription.DoesNotExist:
            Subscription.objects.create(user=user, course=course, subscription=True)
            message = "Подписка добавлена"
            logger.info(f"Url: {request.path} - Subscription of user: {user.email} - course: {course.name}")

        return Response({"message": message})
