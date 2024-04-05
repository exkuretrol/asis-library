from typing import Any

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

READ_PERMISSION = ("view",)
ADD_PERMISSION = ("add",)
ALL_PERMISSION = (
    "change",
    "delete",
)

USER_MODEL = ("account", "customuser")

ADVISOR_MODEL = ("book", "advisor")
AUTHOR_MODEL = ("book", "author")
BOOK_MODEL = ("book", "book")
CIRCULATED_COPY_MODEL = ("book", "circulatedcopy")
COPY_MODEL = ("book", "copy")
KEYWORD_MODEL = ("book", "keyword")
THESIS_MODEL = ("book", "thesis")
BOOK_MODELS = [
    ADVISOR_MODEL,
    AUTHOR_MODEL,
    BOOK_MODEL,
    CIRCULATED_COPY_MODEL,
    COPY_MODEL,
    KEYWORD_MODEL,
    THESIS_MODEL,
]

READ_GROUPS = ["admin", "staff", "advisor", "reader"]
ADD_GROUPS = ["admin", "staff"]
ALL_GROUPS = ["admin"]


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_groups(READ_GROUPS, BOOK_MODELS, READ_PERMISSION)
        create_groups(ADD_GROUPS, BOOK_MODELS, ADD_PERMISSION)
        create_groups(ALL_GROUPS, BOOK_MODELS, ALL_PERMISSION)
        create_groups(
            ALL_GROUPS, [USER_MODEL], READ_PERMISSION + ADD_PERMISSION + ALL_PERMISSION
        )


def create_groups(group_names, model_natural_keys, permissions):
    perm_to_add = []
    for group in group_names:
        print(f"Creating group {group}")
        group, created = Group.objects.get_or_create(name=group)

        for model_natural_key in model_natural_keys:
            for permission in permissions:
                codename = f"{permission}_{model_natural_key[1]}"
                try:
                    p = Permission.objects.get_by_natural_key(
                        codename, *model_natural_key
                    )
                    perm_to_add.append(p)
                    print(f"\t{p.name}")

                except Permission.DoesNotExist:
                    print(f"Permission {codename} does not exist")
                    pass

                except ContentType.DoesNotExist:
                    print(f"Content type {model_natural_key} does not exist")
                    pass
        group.permissions.add(*perm_to_add)
