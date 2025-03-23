from django.db import models
from django.contrib import admin
from core.models.abstract import AuditableModel
from book.models import Book
from django.utils.translation import gettext_lazy as _

class BookName(AuditableModel):
    name = models.CharField(max_length=255)

    book = models.ForeignKey(Book, related_name="book_names", on_delete=models.CASCADE)
    type = models.ForeignKey("classifier.Item", related_name="book_name_types", on_delete=models.DO_NOTHING, limit_choices_to={"type__identifier": "book_name_type"})
    
    class Meta:
        verbose_name = _('Book Name')
        verbose_name_plural = _('Book Names')
        
    def __str__(self):
        return self.name

class BookNameInline(admin.TabularInline):
    model = BookName
    extra = 0
    fields = ["name", "type"]
    can_delete = False
    show_change_link = False
    # classes = ["collapse"]
    verbose_name = _("Book Name")
    verbose_name_plural = _("Book Names")

    formfield_overrides = {
        models.CharField: {
            "widget": admin.widgets.AdminTextInputWidget(attrs={"style": "width: 95%;"})
        },
    }
