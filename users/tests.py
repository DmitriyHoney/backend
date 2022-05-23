from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='admin@mail.ru', phone='+79964456754', password='foo')
        self.assertEqual(user.email, 'admin@mail.ru')
        self.assertEqual(user.phone, '+79964456754')
        self.assertTrue(user.is_active)
        try:
            # проверяем чтобы не было в модели поля username
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(phone='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', phone='', password="foo")
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', phone='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email='super@user.com', phone='+79964456754', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='super@user.com', phone='+79964456754', password='foo', is_superuser=False)