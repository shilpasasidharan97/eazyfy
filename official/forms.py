from .models import UserReply
from django import forms


class SurveyForm(forms.ModelForm):
    class Meta:
        model = UserReply
        fields = "__all__"
        widgets = {"question": forms.HiddenInput(), "option": forms.RadioSelect(attrs={"class": ""})}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["option"].queryset = self.instance.question.get_options()
