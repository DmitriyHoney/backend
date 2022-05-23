from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
# from address.models import AddressInfo
from .managers import UserManager
from django.contrib import admin
from citizen.utils import create_image_thumb
from phonenumber_field.modelfields import PhoneNumberField
# from municipality.models import Municipality


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="Email", unique=True)
    phone = PhoneNumberField(verbose_name="Телефон", unique=True)
    register_date = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()  

    def __str__(self):
        return self.email


# class User(AbstractBaseUser, PermissionsMixin):
#     FEMALE = 'FEMALE'
#     MALE = 'MALE'
#     GENDER = (
#         (FEMALE, 'женский'),
#         (MALE, 'мужской')
#     )
#
#     MARRIED = 1
#     SINGLE = 2
#     MARTIAL_CHOICES = (
#         (MARRIED, 'замужем/женат'),
#         (SINGLE, 'холост/не замужем]')
#     )
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#     objects = UserManager()
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#
#     groups = models.ManyToManyField(Group, verbose_name="Группы пользователя", related_name="user_groups", blank=True)
#     lastname = models.CharField(verbose_name="Фамилия", max_length=30, blank=True)
#     firstname = models.CharField(verbose_name="Имя", max_length=30, blank=True)
#     middlename = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
#     gender = models.CharField(max_length=10, verbose_name="Пол", choices=GENDER, default=MALE)
#     date_of_birth = models.DateField(verbose_name="Дата рождения", auto_now_add=True, blank=True)
#     email = models.EmailField(verbose_name="Email", unique=True)
#     phone = PhoneNumberField(verbose_name="Телефон", unique=True)
#     is_superuser = models.BooleanField(verbose_name="Суперпользователь", default=False)
#     is_archive = models.BooleanField(verbose_name="Пользователь в архиве", default=False)
#     avatar = models.ImageField(verbose_name="Аватар пользователя", upload_to="users/avatars", blank=True)
#     avatar_small = models.ImageField(verbose_name="Аватар пользователя thumb", upload_to="thumbs", blank=True)
#     mo = models.ForeignKey(Municipality, verbose_name="Муниципальное образование пользователя", on_delete=models.SET_NULL, null=True)
#     residential_address = models.OneToOneField(AddressInfo, verbose_name="Адрес проживания", on_delete=models.CASCADE, blank=True, null=True, related_name="residential_address")
#     registration_address = models.OneToOneField(AddressInfo, verbose_name="Адрес регистрации", on_delete=models.CASCADE, blank=True, null=True, related_name="registration_address")
#     property_address = models.OneToOneField(AddressInfo, verbose_name="Адрес собственности", on_delete=models.CASCADE, blank=True, null=True, related_name="property_address")
#     marital_status = models.CharField(max_length=55,  verbose_name="Семейное положение", choices=MARTIAL_CHOICES, default=SINGLE)
#     is_has_childrens = models.BooleanField(verbose_name="Дети есть/нет", default=False)
#     register_date = models.DateTimeField(verbose_name="Дата регистрации", auto_now_add=True, blank=True)
#
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
#
#     @property
#     def is_staff(self):
#         return True
