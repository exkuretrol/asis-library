from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .views import ProfileView, UserLoginView, UserSignupView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
