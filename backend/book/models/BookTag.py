from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.models.abstract import AuditableModel, AuditableAdmin, AuditableModelResource
from book.models import Book
from tag.models import Tag

class BookTag(AuditableModel):
    book = models.ForeignKey(Book, related_name='book_tags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='tag_books', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = '[Book Tag]'
        verbose_name_plural = '[Book Tags]'
            
    def __str__(self):
        return self.tag.name

@admin.register(BookTag)
class BookTagAdmin(AuditableAdmin):
    list_display = ('id', 'book', 'tag', 'active')
