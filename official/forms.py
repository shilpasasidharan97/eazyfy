from .models import QuestionOption
from django import forms


class SurveyForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = "__all__"
