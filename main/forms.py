from .models import Contact
from .models import PhoneOTP
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class PhoneOTPForm(forms.ModelForm):
    class Meta:
        model = PhoneOTP
        fields = ("country_code", "phone_number")
        widgets = {
            "country_code": forms.Select(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
        }
