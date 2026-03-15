from django import forms

from .models.learning_resource import LearningResource
from .models.learning_unit import LearningUnit


class LearningResourceForm(forms.ModelForm):
    class Meta:
        model = LearningResource
        fields = ["title", "resource_type", "description"]


class LearningUnitForm(forms.ModelForm):
    class Meta:
        model = LearningUnit
        fields = ["title", "order", "duration_minutes", "notes"]
