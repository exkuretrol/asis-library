from dal import autocomplete
from django.shortcuts import render

from book.models import Advisor, Author, Keyword


class AdvisorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Advisor.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AuthorAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Author.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class KeywordAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Keyword.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs
