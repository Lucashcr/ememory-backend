from django.forms import Form, CharField, PasswordInput, ValidationError


class ResetPasswordForm(Form):
    new_password = CharField(
        label="Nova senha",
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
        max_length=128,
    )
    re_new_password = CharField(
        label="Confirme a nova senha",
        widget=PasswordInput(attrs={"autocomplete": "new-password"}),
        min_length=8,
        max_length=128,
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        re_new_password = cleaned_data.get("re_new_password")

        if new_password and re_new_password and new_password != re_new_password:
            raise ValidationError("The two password fields didn't match.")

        return cleaned_data
