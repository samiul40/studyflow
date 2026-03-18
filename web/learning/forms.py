from django import forms

from .models.learning_resource import LearningResource
from .models.learning_unit import LearningUnit


class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ["title", "resource_type", "description", "url"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Django Course"}
            ),
            "resource_type": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "url": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://example.com"}
            ),
        }


class LearningUnitForm(forms.ModelForm):
    class Meta:
        model = LearningUnit
        fields = ["title", "duration_minutes", "notes"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "duration_minutes": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "e.g. 15"}
            ),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
