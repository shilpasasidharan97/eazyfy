from django import forms
from .models import UserRequest


class FranchiseAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["franchise"]
