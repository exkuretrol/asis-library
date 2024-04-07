from typing import Iterable

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Value as V
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    no = models.BigAutoField(verbose_name=_("編號"), primary_key=True)
    name = models.CharField(verbose_name=_("姓名"), max_length=255)
    related_user = models.OneToOneField(
        verbose_name=_("關聯使用者"),
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name


class Advisor(models.Model):
    no = models.BigAutoField(verbose_name=_("編號"), primary_key=True)
    name = models.CharField(verbose_name=_("姓名"), max_length=255)
    related_user = models.OneToOneField(
        verbose_name=_("關聯使用者"),
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.name


class CategoryChoices(models.IntegerChoices):
    Thesis = 1, _("論文")
    Book = 2, _("圖書")
    Journal = 3, _("期刊")


class LanguageChoices(models.IntegerChoices):
    English = 1, _("英文")
    Chinese = 2, _("中文")


class Book(models.Model):
    no = models.CharField(verbose_name=_("編號"), primary_key=True, max_length=32)
    title = models.CharField(verbose_name=_("書名"), max_length=255)
    published_date = models.DateField(
        verbose_name=_("出版日"), null=True, blank=True, default=timezone.localdate
    )
    author = models.ManyToManyField(verbose_name=_("作者"), to=Author, blank=True)
    category = models.SmallIntegerField(
        verbose_name=_("類別"),
        choices=CategoryChoices.choices,
        default=CategoryChoices.Book,
    )
    language = models.SmallIntegerField(
        verbose_name=_("語言"),
        choices=LanguageChoices.choices,
        default=LanguageChoices.Chinese,
    )

    def __str__(self):
        return self.no + " - " + self.title


class Keyword(models.Model):
    no = models.BigAutoField(verbose_name=_("編號"), primary_key=True)
    keyword = models.CharField(verbose_name=_("關鍵字"), max_length=255)

    def __str__(self):
        return self.keyword


class DegreeChoices(models.IntegerChoices):
    Bachelor = 1, _("學士")
    Master = 2, _("碩士")


class Thesis(models.Model):
    no = models.BigAutoField(verbose_name=_("編號"), primary_key=True)
    book_no = models.OneToOneField(
        verbose_name=_("書籍編號"),
        to=Book,
        on_delete=models.CASCADE,
    )
    advisor = models.ManyToManyField(verbose_name=_("指導教授"), to=Advisor, blank=True)
    keywords = models.ManyToManyField(verbose_name=_("關鍵字"), to=Keyword, blank=True)
    degree = models.SmallIntegerField(
        verbose_name=_("學位"),
        choices=DegreeChoices.choices,
        default=DegreeChoices.Bachelor,
    )

    @property
    def graduated_year(self):
        try:
            return self.book_no.published_date.year - 1911
        except:
            return f"{self.no} does not have a related book."

    graduated_year.fget.short_description = _("畢業年度")

    @property
    def title(self):
        try:
            return f"{self.book_no.title}"
        except:
            return f"{self.no} does not have a related book."

    title.fget.short_description = _("論文名稱")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "theses"


class StatusChoices(models.IntegerChoices):
    NotLendable = 0, _("不可出借")
    Lendable = 1, _("可出借")
    Lend = 2, _("已借出")
    Lost = 9, _("已遺失")


class Copy(models.Model):
    no = models.BigAutoField(verbose_name=_("副本編號"), primary_key=True)
    book_no = models.ForeignKey(
        verbose_name=_("書籍編號"), to=Book, on_delete=models.CASCADE
    )
    sequence_no = models.PositiveSmallIntegerField(verbose_name=_("序號"), default=0)
    status = models.PositiveSmallIntegerField(
        verbose_name=_("狀態"),
        choices=StatusChoices.choices,
        default=StatusChoices.Lendable,
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("建立時間"), auto_now_add=True
    )
    update_datetime = models.DateTimeField(
        verbose_name=_("上次更新時間"), auto_now=True
    )
    maintainer = models.ForeignKey(
        verbose_name=_("維護者"),
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.book_no.no}-{self.sequence_no}"

    class Meta:
        verbose_name_plural = "copies"
        constraints = [
            models.UniqueConstraint(
                fields=["book_no", "sequence_no"], name="unique_book_sequence_no"
            )
        ]

    def save(self, *args, **kwargs):
        if self.sequence_no == 0:
            self.sequence_no = Copy.objects.filter(book_no=self.book_no).count() + 1
        super().save(*args, **kwargs)


class FineStatusChoices(models.IntegerChoices):
    Pending = 1, _("待繳")
    Settled = 2, _("已結清")
    NotApplicable = 9, _("不適用")


class CirculatedCopy(models.Model):
    def default_return_date():
        return timezone.localdate() + timezone.timedelta(days=7)

    no = models.BigAutoField(verbose_name=_("編號"), primary_key=True)
    reader_no = models.ForeignKey(
        verbose_name=_("讀者"), to=get_user_model(), on_delete=models.CASCADE
    )
    copy_no = models.ForeignKey(
        verbose_name=_("副本編號"), to=Copy, on_delete=models.CASCADE
    )
    borrowed_date = models.DateField(
        verbose_name=_("借閱日"), default=timezone.localdate
    )
    due_date = models.DateField(
        verbose_name=_("到期日"),
        default=default_return_date,
    )
    return_date = models.DateField(verbose_name=_("歸還日"), null=True, blank=True)

    fine_status = models.PositiveSmallIntegerField(
        verbose_name=_("罰金狀態"),
        choices=FineStatusChoices.choices,
        default=FineStatusChoices.NotApplicable,
    )

    @property
    def fine_amount(self):
        unit = 10
        if self.return_date is None:
            return 0
        return max(0, (self.return_date - self.due_date).days) * unit

    fine_amount.fget.short_description = _("罰金")

    class Meta:
        verbose_name_plural = "circulated copies"
