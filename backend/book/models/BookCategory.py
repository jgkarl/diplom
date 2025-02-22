from django.db import models
from core.models.abstract import AuditableModel
from book.models import Book

class BookCategory(AuditableModel):
    book = models.ForeignKey(Book, related_name='book_categories', on_delete=models.CASCADE)
    type = models.ForeignKey('classifier.Item', related_name='book_category_types', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'book_category'} )

    class Meta:
        verbose_name = 'TEST[Book Category]'
        verbose_name_plural = '[Book Categories]'
            
    def __str__(self):
        return self.type.name