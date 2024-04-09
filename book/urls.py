from django.urls import path

from .views import BookDetailView, BookListView, BookUpdateView

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("<str:pk>/", BookDetailView.as_view(), name="book_detail"),
]
