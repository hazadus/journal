from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with additional fields.
    """

    second_name = models.CharField(verbose_name="Отчество", max_length=16)
    birthday = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    avatar_img = models.ImageField(
        verbose_name="Аватар профиля", null=True, blank=True, upload_to="images/"
    )
    notes = models.TextField(verbose_name="Заметки", null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def short_name(self):
        """
        Return short user name, i.e. "Иванов И.И." for "Иванов Иван Иванович"
        """
        return "{surname} {name_letter}{second_name_letter}".format(
            surname=self.last_name,
            name_letter=self.first_name[:1] + "." if self.first_name else "",
            second_name_letter=self.second_name[:1] + "." if self.second_name else "",
        )
