from official.models import UserRequest

from django import forms


class PickupAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["pickupboy"]
