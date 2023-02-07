from .models import Contact, PhoneOTP
from django.forms import ModelForm


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class PhoneOTPForm(ModelForm):
    class Meta:
        model = PhoneOTP
        fields = ("country_code", "phone_number")
