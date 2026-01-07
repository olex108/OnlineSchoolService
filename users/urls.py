from django.urls import path

from . import views
from .apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path("register/", views.UserRegisterAPIView.as_view(), name="register"),
    path("users/email_confirm/<str:token>/", views.UserEmailVerificationAPIView.as_view(), name="email_confirm"),
    path("users/<int:pk>/", views.UserRetrieveAPIView.as_view(), name="user-get"),
    path("users/<int:pk>/update/", views.UserUpdateAPIView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDestroyAPIView.as_view(), name="user-delete"),
    # payment paths
    path("payment/", views.PaymentListAPIView.as_view(), name="payment-list"),
]
