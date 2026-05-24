from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm as DjangoPasswordChangeForm,
)

User = get_user_model()

_FC = {"class": "form-control"}


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs=_FC),
            "last_name": forms.TextInput(attrs=_FC),
            "email": forms.EmailInput(attrs=_FC),
        }
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class ChangePasswordForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(_FC)
