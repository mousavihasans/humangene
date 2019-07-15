from enum import IntEnum
from datetime import timedelta, datetime

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from utils.intenum import IntEnumField


class MemberManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class Member(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    profile_picture = models.ImageField(upload_to='images/profiles', blank=True, null=True)

    confirmed = models.BooleanField(default=False)

    credit = models.IntegerField(default=0, help_text="واحد ریال - IRR")

    objects = MemberManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email + "-" + '%s %s' % (self.first_name, self.last_name)

    @property
    def display_name(self):
        result = 'بی نام'
        if self.first_name or self.last_name:
            result = self.first_name + " " + self.last_name
        return result


#
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to="images/profile_pictures", blank=True, null=True)
#     credit = models.IntegerField(default=0, help_text="واحد ریال - IRR")
#
#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#
#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class IncreaseCreditViaBankChoices(IntEnum):
    success = 0
    failed = 1


class IncreaseCreditViaBank(models.Model):
    amount = models.IntegerField(default=20000000, help_text='Unit is IRR')
    status = IntEnumField(IncreaseCreditViaBankChoices, default=IncreaseCreditViaBankChoices.success)
    tracking_code = models.CharField(max_length=200)

    # post save bezanam vase afzayesh etebar!!??


@receiver(post_save, sender=Member)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)