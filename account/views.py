from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationForm, UserLoginForm


class UserSignupView(CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")


class UserLoginView(LoginView):
    template_name = "login.html"
    form_class = UserLoginForm
