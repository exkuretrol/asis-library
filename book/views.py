import django_tables2 as tables
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView

from .filters import BookFilter
from .models import Book
from .tables import BookTable


class BookListView(tables.SingleTableMixin, FilterView):
    table_class = BookTable
    model = Book
    filterset_class = BookFilter
    template_name = "book_list.html"


class BookUpdateView(UpdateView):
    model = Book
    fields = "__all__"
    template_name = "book_update.html"
    success_url = "/book/"


class BookDetailView(DetailView):
    template_name = "book_detail.html"
    model = Book
    fields = "__all__"
