from django.contrib import admin
from django.db import models
from core.models.abstract import AuditableModel
from book.models import Book


class BookExtra(AuditableModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    book = models.ForeignKey(Book, related_name="book_extras", on_delete=models.CASCADE)
    type = models.ForeignKey(
        "classifier.Item",
        related_name="book_extra_types",
        on_delete=models.DO_NOTHING,
        limit_choices_to={"type__identifier": "book_extra_type"},
    )

    def __str__(self):
        return self.type.name


class BookExtraInline(admin.TabularInline):
    model = BookExtra
    extra = 0
    fields = [
        "name",
        "type",
        "description",
    ]
    can_delete = False
    show_change_link = False
    # classes = ["collapse"]

    formfield_overrides = {
        models.CharField: {
            "widget": admin.widgets.AdminTextInputWidget(attrs={"style": "width: 95%;"})
        },
        models.TextField: {
            "widget": admin.widgets.AdminTextareaWidget(
                attrs={"style": "width: 95%;", "rows": 2}
            )
        },
    }
