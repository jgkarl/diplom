from django.contrib import admin
from django.db import models
from core.models.abstract import AuditableModel
from book.models import Book


class BookResume(AuditableModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # conditional boolean, in order to concretely indicate if resume is present at all
    has_resume = models.BooleanField(null=True, blank=True)
    notes = models.TextField()

    book = models.ForeignKey(
        Book, related_name="book_resumes", on_delete=models.CASCADE
    )
    language = models.ForeignKey(
        "classifier.Item",
        related_name="book_resume_language_types",
        on_delete=models.DO_NOTHING,
        limit_choices_to={"type__identifier": "language"},
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name}"


class BookResumeInline(admin.TabularInline):
    model = BookResume
    extra = 0
    fields = ["name", "language", "has_resume"]
    can_delete = False
    show_change_link = False
    # classes = ["collapse"]

    formfield_overrides = {
        models.CharField: {
            "widget": admin.widgets.AdminTextInputWidget(
                attrs={"style": "width: 95%;"}
            )
        },
    }
