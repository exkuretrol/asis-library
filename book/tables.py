import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from .models import Book, CategoryChoices


class BookTable(tables.Table):
    published_date = tables.Column(accessor="published_date", verbose_name="出版年")
    degree = tables.Column(accessor="thesis__degree", verbose_name="學位")

    def is_thesis(self, request):
        return (
            "category" in request.GET
            and request.GET["category"].isdigit()
            and int(request.GET.get("category")) == CategoryChoices.Thesis
        )

    def render_published_date(self, value):
        return value.strftime("%Y")

    def render_title(self, record, value):
        if record.category == CategoryChoices.Thesis:
            authors = record.author.all()
            authors_str = "、".join([author.name for author in authors])
            advisors = record.thesis.advisor.all()
            advisors_str = "、".join([advisor.name for advisor in advisors])

            return format_html(
                f"""
                <strong><a href="{reverse(viewname="book_detail", kwargs={"pk": record.pk})}">{value}</a></strong>
                <p>作者：{authors_str}</p>
                <p>指導教授：{advisors_str}</p>
            """
            )

        else:
            return value

    def before_render(self, request):
        if self.is_thesis(request):
            self.columns.show("degree")
        else:
            self.columns.hide("degree")

        return super().before_render(request)

    class Meta:
        fields = ("title", "published_date", "category")
        model = Book
        order_by = ("-published_date",)
