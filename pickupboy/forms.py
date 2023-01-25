from official.models import PickupData

from django import forms


class PickupCompleteForm(forms.ModelForm):
    class Meta:
        model = PickupData
        fields = (
            "imei_number",
            "front_image",
            "back_image",
            "top_image",
            "bottom_image",
            "right_image",
            "left_image",
            "selfie_image",
        )
        widgets = {
            "imei_number": forms.TextInput(attrs={"class": "form-control", "accept": "image/*", "capture": "camera"}),
            "front_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "back_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "top_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "bottom_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "right_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "left_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
            "selfie_image": forms.FileInput(
                attrs={"class": "form-control preview", "accept": "image/*", "capture": "camera"}
            ),
        }
        labels = {
            "imei_number": "IMEI Number",
            "front_image": " ",
            "back_image": " ",
            "top_image": " ",
            "bottom_image": " ",
            "right_image": " ",
            "left_image": " ",
            "selfie_image": " ",
        }
        help_texts = {
            "front_image": "Front Image",
            "back_image": "Back Image",
            "top_image": "Top Image",
            "bottom_image": "Bottom Image",
            "right_image": "Right Image",
            "left_image": "Left Image",
            "selfie_image": "Selfie with Customer",
        }


class PickupFailForm(forms.ModelForm):
    class Meta:
        model = PickupData
        fields = ("remarks",)
        widgets = {
            "remarks": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter Remarks", "rows": "3", "style": "height:150px"}
            )
        }
