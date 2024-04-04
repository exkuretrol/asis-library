from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Advisor, Author, Book, CirculatedCopy, Copy, Keyword, Thesis


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("no", "title", "published_date", "category", "language")
    list_filter = ("category", "language")
    search_fields = ("title",)
    date_hierarchy = "published_date"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("no", "name")
    search_fields = ("name",)


@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ("no", "name")
    search_fields = ("name",)


@admin.register(Copy)
class CopyAdmin(admin.ModelAdmin):
    list_display = ("no", "book_no", "sequence_no", "status")
    list_filter = ("status",)
    search_fields = ("book_no__title",)


@admin.register(CirculatedCopy)
class CirculatedCopyAdmin(admin.ModelAdmin):
    list_display = (
        "copy_no",
        "reader_no",
        "borrowed_date",
        "due_date",
        "return_date",
        "fine_amount",
        "fine_status",
    )
    list_filter = ("borrowed_date", "return_date", "fine_status")
    search_fields = ("copy_no__book_no__title",)


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("no", "keyword")
    search_fields = ("keyword",)


class GraduatedYearListFilter(admin.SimpleListFilter):
    title = _("畢業年度")
    parameter_name = "year"
    dept_start_year = 1990 + 10
    dept_this_year = timezone.now().year

    def lookups(self, request, model_admin):
        return (
            (year, str(year - 1911))
            for year in range(self.dept_start_year, self.dept_this_year + 1)
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(book__published_date__year=self.value())


@admin.register(Thesis)
class ThesisAdmin(admin.ModelAdmin):
    list_display = ("no", "title", "graduated_year")
    list_filter = ("advisor", GraduatedYearListFilter)
    list_display_links = ("no", "title")
    search_fields = ("title",)
