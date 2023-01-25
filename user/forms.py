from official.models import UserRequest

from django import forms


class UserRequestInfoForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["name", "phone", "address", "city", "pincode"]
