import random

from .models import PhoneOTP
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
import urllib


def custom_redirect(url_name, *args, **kwargs):
    url = reverse(url_name, args=args)
    # keep / in url
    query_string = urllib.parse.urlencode(kwargs)
    query_string = query_string.replace("%2F", "/")
    url = f"{url}?{query_string}"
    return HttpResponseRedirect(url)


def send_otp(otp_instance):
    phone_number = f"{otp_instance.country_code}{otp_instance.phone_number}"
    otp = otp_instance.otp
    print(phone_number, otp)
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
