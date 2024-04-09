from django.urls import path

from .views import AdvisorAutocomplete, AuthorAutocomplete, KeywordAutocomplete

urlpatterns = [
    path("advisor/", AdvisorAutocomplete.as_view(), name="advisor_autocomplete"),
    path("author/", AuthorAutocomplete.as_view(), name="author_autocomplete"),
    path("keyword/", KeywordAutocomplete.as_view(), name="keyword_autocomplete"),
]
