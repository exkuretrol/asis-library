import django_tables2 as tables
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django_tables2.views import SingleTableMixin

from book.tables import BookTable

from .forms import UserCreationForm, UserLoginForm
from .tables import ThesisTable


class UserSignupView(CreateView):
    template_name = "signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")


class UserLoginView(LoginView):
    template_name = "login.html"
    form_class = UserLoginForm


def is_role(user, role):
    return user.groups.filter(name=role).exists()


class ProfileView(SingleTableMixin, TemplateView):
    template_name = "profile.html"

    def get_table_class(self):
        if is_role(self.request.user, "advisor"):
            return ThesisTable
        elif is_role(self.request.user, "reader"):
            return BookTable
        return tables.Table

    def get_queryset(self):
        qs = ()
        if is_role(self.request.user, "advisor"):
            qs = self.request.user.advisor.thesis_set.all()
        elif is_role(self.request.user, "reader"):
            qs = self.request.user.author.book_set.all()
        return qs
