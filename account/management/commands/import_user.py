from collections import Counter
from pathlib import Path
from typing import Any

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandParser

from account.models import CustomUser
from book.models import Advisor, Author


class Command(BaseCommand):
    help = "Import users from csv file"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--csv", type=str, help="CSV file path")
        parser.add_argument("--type", type=str, help="Type of user")
        return super().add_arguments(parser)

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write("Importing users...")

        cmd_execute_path = Path().cwd()
        file_path = cmd_execute_path / options["csv"]
        parse_csv(self, options["type"], file_path)


def empty():
    CustomUser.objects.all().delete()


def parse_csv(self, user_type, file_path: Path):
    import pandas as pd

    empty()

    df = pd.read_csv(file_path)
    if df.duplicated(subset=["id"]).any():
        df.drop_duplicates(subset=["id"], inplace=True)
    admin = Group.objects.get(name="admin")
    staff = Group.objects.get(name="staff")
    advisor = Group.objects.get(name="advisor")
    reader = Group.objects.get(name="reader")

    for index, row in df.iterrows():
        name_list = list(row["name"])
        last_name = name_list[0]
        first_name = "".join(name_list[1:])
        password = row["psd"] if "psd" in row else "not_secure_please_change_it"

        if CustomUser.objects.filter(username=row["id"]).exists():
            print(f"User {row['id']} already exists appending to group {user_type}...")
            user = CustomUser.objects.get(username=row["id"])
        else:
            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=row["id"],
                email=row["id"] + "@" + settings.EMAIL_DOMAIN,
                password=password,
            )
            user.save()

        if user_type == "staff":
            if row["admin"] == 1:
                admin.user_set.add(user)
            else:
                staff.user_set.add(user)
        elif user_type == "reader":
            if row["teacher or not"] == "O":
                advisor.user_set.add(user)
                Advisor.objects.create(name=last_name + first_name, related_user=user)
            else:
                reader.user_set.add(user)
                Author.objects.create(name=last_name + first_name, related_user=user)
