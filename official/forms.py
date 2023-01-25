from .models import UserRequest
from django import forms


class FranchiseAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["franchise", "final_amount"]
