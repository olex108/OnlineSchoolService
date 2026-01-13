from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса", unique=True)
    preview = models.ImageField(upload_to="images/", verbose_name="Превью(Изображение)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True)
    video_url = models.URLField(verbose_name="Ссылка на материалы", null=True, blank=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Владелец курса")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        ordering = ["name"]


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока")
    preview = models.ImageField(upload_to="images/", verbose_name="Превью(Изображение)", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", null=True)
    video_url = models.URLField(verbose_name="Ссылка на материалы", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, verbose_name="Владелец урока")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["name"]
