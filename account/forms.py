from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
