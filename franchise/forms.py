from django import forms
from official.models import UserRequest


class PickupAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["pickupboy"]
