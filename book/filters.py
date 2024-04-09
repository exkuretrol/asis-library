import django_filters as filters
from dal import autocomplete
from django.utils.translation import gettext_lazy as _

from .models import Advisor, Author, Book, Keyword


class BookFilter(filters.FilterSet):
    def advisor_filter(self, queryset, name, value):
        return queryset.filter(thesis__advisor__name__icontains=value)

    def keyword_filter(self, queryset, name, value):
        return queryset.filter(thesis__keywords__keyword__icontains=value)

    title__icontains = filters.CharFilter(
        label=_("論文標題"), field_name="title", lookup_expr="icontains"
    )
    author = filters.ModelChoiceFilter(
        label=_("作者"),
        queryset=Author.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="author_autocomplete", attrs={"data-placeholder": _("輸入作者名稱")}
        ),
    )

    thesis_advisor = filters.ModelChoiceFilter(
        label=_("指導老師"),
        field_name="thesis_advisor",
        method="advisor_filter",
        queryset=Advisor.objects.all(),
        widget=autocomplete.ModelSelect2(
            url="advisor_autocomplete",
            attrs={"data-placeholder": _("輸入指導老師名稱")},
        ),
    )

    thesis_keyword = filters.CharFilter(
        label=_("關鍵詞"),
        field_name="thesis_keyword",
        method="keyword_filter",
    )

    class Meta:
        model = Book
        fields = ("category", "language", "author")
