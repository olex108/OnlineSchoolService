from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


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

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    payment_date = models.DateTimeField(verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(Course, verbose_name="Оплаченный курс", on_delete=models.CASCADE, null=True)
    paid_lesson = models.ForeignKey(Lesson, verbose_name="Оплаченный урок", on_delete=models.CASCADE, null=True)
    amount = models.FloatField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    def __str__(self) -> str:
        return f"{self.user} - {self.paid_course}{self.paid_lesson} - {self.payment_date} - {self.amount}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["payment_date"]


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
