from django import forms
from official.models import UserRequest


class UserRequestInfoForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["name", "phone", "address", "city", "pincode"]
