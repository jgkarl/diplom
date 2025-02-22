from django.db import models
from core.models.abstract import AuditableModel 
from book.models import Book

class BookLanguage(AuditableModel):
    book = models.ForeignKey(Book, related_name='book_languages', on_delete=models.CASCADE)
    type = models.ForeignKey('classifier.Item', related_name='book_language_types', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'language'} )
    
    class Meta:
        verbose_name = '[Book Language]'
        verbose_name_plural = '[Book Languages]'
      
    def __str__(self):
        return self.type.name
