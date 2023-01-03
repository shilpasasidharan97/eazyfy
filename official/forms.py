from django import forms
from .models import QuestionOption


class SurveyForm(forms.ModelForm):
    class Meta:
        model = QuestionOption
        fields = "__all__"
