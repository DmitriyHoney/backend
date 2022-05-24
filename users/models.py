from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin, Group
from .managers import UserManager
from citizen.utils import create_image_thumb
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    FEMALE = 'FEMALE'
    MALE = 'MALE'
    GENDER = (
        (FEMALE, 'женский'),
        (MALE, 'мужской')
    )

    MARRIED = 'MARRIED'
    SINGLE = 'SINGLE'
    MARTIAL_CHOICES = (
        (MARRIED, 'замужем/женат'),
        (SINGLE, 'холост/не замужем]')
    )

    email = models.EmailField(verbose_name="Email", unique=True)
    phone = PhoneNumberField(verbose_name="Телефон", unique=True, null=True)
    register_date = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, verbose_name="Группы пользователя", related_name="user_groups", blank=True)
    lastname = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
    firstname = models.CharField(verbose_name="Имя", max_length=30, blank=True)
    middlename = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
    gender = models.CharField(max_length=10, verbose_name="Пол", choices=GENDER, default=MALE)
    date_of_birth = models.DateField(verbose_name="Дата рождения", auto_now_add=True, blank=True)
    avatar = models.ImageField(verbose_name="Аватар пользователя", upload_to="users/avatars", blank=True)
    avatar_small = models.ImageField(verbose_name="Аватар пользователя thumb", upload_to="thumbs", blank=True)

    # residential_address = models.OneToOneField(AddressInfo, verbose_name="Адрес проживания", on_delete=models.CASCADE, blank=True, null=True, related_name="residential_address")
    # registration_address = models.OneToOneField(AddressInfo, verbose_name="Адрес регистрации", on_delete=models.CASCADE, blank=True, null=True, related_name="registration_address")
    # property_address = models.OneToOneField(AddressInfo, verbose_name="Адрес собственности", on_delete=models.CASCADE, blank=True, null=True, related_name="property_address")
    marital_status = models.CharField(max_length=55,  verbose_name="Семейное положение", choices=MARTIAL_CHOICES, default=SINGLE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'

    objects = UserManager()  

    def __str__(self):
        return self.email

    def create_avatar_thumb(self, new_avatar):
        self.avatar_small.delete(save=True)
        self.avatar.delete(save=True)
        if new_avatar:
            self.avatar = new_avatar
            create_image_thumb(self, self.avatar, self.avatar_small)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = reset_password_token.key
    send_mail(
        # title:
        "Сброс пароля для портала Тестовый портал",
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )


# class User(AbstractBaseUser, PermissionsMixin):
#     def is_admin(self):
#         return any(g.name == 'admin' for g in self.groups.all())
#
#     def is_moderator(self):
#         return any(g.name == 'moderator' for g in self.groups.all())
#
#     def is_user(self):
#         return any(g.name == 'user' for g in self.groups.all())
#
#     @admin.display(description='Группы пользователя')
#     def get_groups(self):
#         return '; '.join([g.name for g in self.groups.all()])
#
#     @admin.display(description='ФИО')
#     def get_full_name(self):
#         """
#         Returns the FIO
#         """
#         full_name = f"{self.lastname} {self.firstname} {self.middlename}"
#         return full_name.strip()
#
#     def get_short_name(self):
#         """
#         Returns the short name for the user.
#         """
#         full_name = f"{self.lastname} {self.firstname[0] if self.firstname else '-'} {self.middlename[0] if self.middlename else '-'}"
#         return full_name.strip()
#
#     def create_avatar_thumb(self):
#         self.avatar_small.delete(save=True)
#         if self.avatar:
#             create_image_thumb(self, self.avatar, self.avatar_small)
