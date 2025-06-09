from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not phone:
            raise ValueError(_("The Email must be set"))
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):
    phone = models.CharField(max_length=13, unique=True)
    username = models.CharField(max_length=150)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def save(self, **kwargs):
        if self.username:
            existing_users = User.objects.filter(username=self.username)
            if existing_users:
                raise ValueError(_("username already exists"))
        return super().save(**kwargs)
    
    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=19)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=2)
    cvc = models.CharField(max_length=3)
    added_at = models.DateTimeField(auto_now_add=True)


    def masked_number(self):
        # Возвращает номер карты с маской, например "**** **** **** 1234"
        return "**** **** **** " + self.card_number[-4:]

    def __str__(self):
        return f"{self.masked_number()} (User: {self.user.username})"