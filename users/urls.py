from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .apps import UsersConfig
from rest_framework.permissions import AllowAny

from .views import SubscribeAPIView

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("users/email_confirm/<str:token>/", views.UserEmailVerificationAPIView.as_view(), name="email-confirm"),
    path("users/<int:pk>/", views.UserRetrieveAPIView.as_view(), name="user-get"),
    path("users/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDestroyAPIView.as_view(), name="user-delete"),
    # token
    path("login/", TokenObtainPairView.as_view(permission_classes=[AllowAny]), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # payment paths
    path("payment/", views.PaymentListAPIView.as_view(), name="payment-list"),
    path("payment/create/", views.PaymentCreateAPIView.as_view(), name="payment-create"),
    path("payment/<int:pk>/", views.PaymentRetrieveAPIView.as_view(), name="payment-detail"),
    # subscribe
    path("subscribe/<int:pk>/", SubscribeAPIView.as_view(), name="subscribe"),
]
