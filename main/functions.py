import random

from .models import PhoneOTP
from django.core.exceptions import ValidationError
from django.utils import timezone


def send_otp(phone_number):
    otp = str(random.randint(100000, 999999))
    PhoneOTP.objects.create(phone_number=phone_number, otp=otp)
    # send the OTP to the user's phone number
    # you can use a third-party API or your own SMS gateway
    return otp


def verify_otp(phone_number, otp):
    try:
        phone_otp = PhoneOTP.objects.get(phone_number=phone_number, otp=otp)
        if (timezone.now() - phone_otp.created_at).total_seconds() > 300:
            raise ValidationError("OTP expired")
        return True
    except PhoneOTP.DoesNotExist:
        return False
