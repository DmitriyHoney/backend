from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone, password, **extra_fields):
        """
        Custom user model manager where email and phone is the unique identifiers
        for authentication instead of usernames.
        """
        if not email:
            raise ValueError('The Email must be set')
        if not phone:
            raise ValueError('The Phone must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        """
            Create and save a SuperUser with the given email, phone and password.
        """
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user(email, phone, password, **extra_fields)