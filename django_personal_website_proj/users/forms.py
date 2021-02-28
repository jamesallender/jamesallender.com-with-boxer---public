from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    # display_name = forms.CharField
    # authorize = forms.CheckboxInput

    class Meta:
        model = User
        # fields = ['username', 'display_name', 'email', 'password1', 'password2', 'authorize']
        fields = ['username', 'email', 'password1', 'password2']
