from .models import Contact
from django.forms import ModelForm
from official.models import User


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
