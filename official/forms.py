from .models import UserRequest, FranchiseWallet
from django import forms


class FranchiseAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["franchise", "final_amount"]


class AddAmountForm(forms.ModelForm):
    class Meta:
        model = FranchiseWallet
        fields = ["franchise", "amount"]
