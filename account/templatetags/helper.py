from django import template

from account.models import CustomUser
from book.models import Thesis

register = template.Library()


@register.filter
def is_advisor(user: CustomUser):
    return user.groups.filter(name="advisor").exists()


@register.filter
def is_reader(user: CustomUser):
    return user.groups.filter(name="reader").exists()


@register.simple_tag
def is_current_thesis_advisor(user: CustomUser, thesis: Thesis):
    return thesis.advisor.filter(related_user=user).exists()
