from .models import FranchiseWallet
from .models import UserRequest
from django import forms


class FranchiseAssignForm(forms.ModelForm):
    class Meta:
        model = UserRequest
        fields = ["franchise", "final_amount"]


class AddAmountForm(forms.ModelForm):
    class Meta:
        model = FranchiseWallet
        fields = ["franchise", "amount"]
