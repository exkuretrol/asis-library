from datetime import datetime
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandParser

from account.models import CustomUser
from book.models import (
    Author,
    Book,
    CategoryChoices,
    Copy,
    DegreeChoices,
    Keyword,
    LanguageChoices,
    StatusChoices,
    Thesis,
)


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser):
        parser.add_argument("--csv", type=str, help="CSV file path")

    def handle(self, **options):
        self.stdout.write("Importing users...")

        cmd_execute_path = Path().cwd()
        file_path = cmd_execute_path / options["csv"]
        parse_csv(self, file_path)


def empty():
    Book.objects.all().delete()
    Copy.objects.all().delete()
    Thesis.objects.all().delete()


def parse_csv(self, file_path: Path):

    empty()

    col_types = {
        "bookID": str,
        "bookname": str,
        "lend it or not": str,
        "categoryID": int,
        "updater": str,
        "prefix": str,
    }

    df = pd.read_csv(file_path, dtype=col_types, parse_dates=["update"])
    for index, row in df.iterrows():

        if row["categoryID"] == 1:
            cate = CategoryChoices.Thesis
            lang = LanguageChoices.Chinese

            try:
                book = Book.objects.get(no=row["bookID"])
            except Book.DoesNotExist:
                import re

                result = re.match(r"^(\d{2,3})(\d{2})$", str(row["bookID"]))
                published_year = 1911 + int(result.groups()[0])

                book = Book.objects.create(
                    no=row["bookID"],
                    title=row["bookname"],
                    category=cate,
                    language=lang,
                    published_date=datetime(published_year + 1, 6, 30).date(),
                )
                book.save()

            if cate == CategoryChoices.Thesis:
                if "prefix" in row:
                    degree = DegreeChoices.Master
                else:
                    degree = DegreeChoices.Bachelor
                thesis, _ = Thesis.objects.get_or_create(
                    book_no=book,
                    degree=degree,
                )

            status = (
                StatusChoices.Lendable
                if row["lend it or not"] == "O"
                else StatusChoices.NotLendable
            )

            try:
                maintainer = CustomUser.objects.get(full_name=row["updater"].strip())
            except maintainer.DoesNotExist:
                maintainer = CustomUser.objects.get(full_name="統資系系辦")
                print(f"User {row['updater']} not found")

            copy = Copy.objects.create(
                book_no=book,
                status=status,
                create_datetime=row["update"],
                update_datetime=row["update"],
                maintainer=maintainer,
            )

            copy.save()

        elif row["categoryID"] == 6 or row["categoryID"] == 7:
            cate = CategoryChoices.Journal
        else:
            cate = CategoryChoices.Book
