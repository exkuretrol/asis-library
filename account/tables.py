import django_tables2 as tables
from django.utils.translation import gettext_lazy as _

from book.models import Thesis


class ThesisTable(tables.Table):
    graduated_year = tables.Column(verbose_name=_("畢業年度"))
    title = tables.Column(verbose_name=_("論文名稱"))

    class Meta:
        model = Thesis
        fields = (
            "title",
            "degree",
            "graduated_year",
        )
