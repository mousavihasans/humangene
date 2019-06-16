from enum import IntEnum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from utils.intenum import IntEnumField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/profile_pictures", blank=True, null=True)
    credit = models.IntegerField(default=0, help_text="واحد ریال - IRR")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class IncreaseCreditViaBankChoices(IntEnum):
    success = 0
    failed = 1


class IncreaseCreditViaBank(models.Model):
    amount = models.IntegerField(default=20000000, help_text='Unit is IRR')
    status = IntEnumField(IncreaseCreditViaBankChoices, default=IncreaseCreditViaBankChoices.success)
    tracking_code = models.CharField(max_length=200)

    # post save bezanam vase afzayesh etebar!!??



