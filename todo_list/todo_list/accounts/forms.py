from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class EditUserForm(auth_forms.UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
        field_classes = {
            'username': auth_forms.UsernameField,
        }


class NewUserForm(auth_forms.UserCreationForm):
    username = forms.CharField(
        max_length=50,
    )
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ("username", "email")
        field_classes = {
            'username': auth_forms.UsernameField,
        }

    def clean(self):
        cleaned_data = super(NewUserForm, self).clean()
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if not password1:
            raise ValidationError('You must confirm your password.')

        if password1 != password2:
            raise ValidationError('Your passwords did not match.')

        return cleaned_data
