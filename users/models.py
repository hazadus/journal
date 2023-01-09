from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    second_name = models.CharField(verbose_name="Отчество", max_length=16)
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    avatar_img = models.ImageField(verbose_name="Аватар профиля", null=True, blank=True, upload_to='images/')
    notes = models.TextField(verbose_name="Заметки", null=True, blank=True)

    def __str__(self):
        return self.username
