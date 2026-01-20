from datetime import datetime, timezone

from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.serializers import ValidationError

from config.settings import STRIPE_API_KEY
from courses.models import Course, Lesson
from users.src.transfer_api_service import StripeAPIService


class User(AbstractUser):
    """
    Model of user representing with field email for authentication of user

    Field  from AbstractUser model
    id: id of user
    password: password
    last_login:
    is_superuser:
    first_name:
    last_name:
    is_staff:
    is_active:
    date_joined:

    Added fields for project
    email: email address of user is uniq field
    phone: phone number in formate "+XXXXXXXXXXX"
    country: country in charfield formate
    avatar: image of useer
    token: token to verification of user email
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=15, verbose_name="Телефон", null=True)
    country = models.CharField(max_length=32, verbose_name="Страна", help_text="страна", blank=True, null=True)
    avatar = models.ImageField(
        upload_to="users/avatar/", verbose_name="Аватар", help_text="Загрузите аватар", blank=True, null=True
    )

    token = models.CharField(max_length=100, verbose_name="Token", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    """Model of payment"""

    PAYMENT_METHOD_CHOICES = (("CASH", "наличные"), ("TRANSFER", "перевод на счет"))
    PAYMENT_STATUS_CHOICES = (("CREATED", "создан"), ("PAID", "оплачен"))

    owner = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    payment_date = models.DateTimeField(verbose_name="Дата оплаты", blank=True, null=True)
    paid_course = models.ForeignKey(
        Course, verbose_name="Оплаченный курс", on_delete=models.CASCADE, null=True, blank=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, verbose_name="Оплаченный урок", on_delete=models.CASCADE, null=True, blank=True
    )
    amount = models.FloatField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")
    payment_status = models.CharField(
        max_length=8, choices=PAYMENT_STATUS_CHOICES, verbose_name="Статус оплаты", default="CREATED"
    )

    def __str__(self) -> str:
        return f"{self.owner} - {self.paid_course}{self.paid_lesson} - {self.payment_date} - {self.amount}"

    def clean(self):
        super().clean()
        if self.paid_course is None and self.paid_lesson is None:
            raise ValidationError("Должен быть заполнен либо 'paid_course', либо 'paid_lesson'.")
        if self.paid_course is not None and self.paid_lesson is not None:
            raise ValidationError("Заполните только одно из полей: 'paid_course' или 'paid_lesson'.")
        if self.paid_course is None and self.paid_lesson is None:
            raise ValidationError("Заполните одно из полей 'paid_course' или 'paid_lesson'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def update_status(self):
        """Method to update payment status and payment_date of payment"""

        if self.payment_status == "CREATED" and self.payment_method == "TRANSFER":
            transfer = self.transfer_set.first()
            transfer_service = StripeAPIService(STRIPE_API_KEY)
            retrieve = transfer_service.retrieve_session(transfer.session_id)
            if retrieve.get("payment_status") == "paid":
                self.payment_status = "PAID"
                self.payment_date = datetime.now(timezone.utc)

            self.save()

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["payment_date"]

        # New object must have one of fields paid_course or paid_lesson
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(paid_course__isnull=False, paid_lesson__isnull=True)
                    | models.Q(paid_course__isnull=True, paid_lesson__isnull=False)
                ),
                name="only_one_product_type_check",
            )
        ]


class Transfer(models.Model):
    """Model of transfer"""

    payment = models.ForeignKey(Payment, verbose_name="Платеж", on_delete=models.CASCADE)
    link = models.URLField(verbose_name="Ссылка на оплату", null=True, blank=True, max_length=500)
    session_id = models.CharField(max_length=100, verbose_name="Сессия")
    price_id = models.CharField(max_length=100, verbose_name="Цена")
    product_id = models.CharField(max_length=100, verbose_name="Продукт")

    def __str__(self) -> str:
        return f"{self.payment} - {self.link}"

    class Meta:
        verbose_name = "перевод"
        verbose_name_plural = "переводы"
        ordering = ["payment"]


class Subscription(models.Model):
    """Model of subscription"""

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)
    subscription = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self) -> str:
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
        ordering = ["course"]
