from django.db import models
from core.models.abstract import AuditableModel

class Book(AuditableModel):    
    token = models.CharField(max_length=64, null=True, blank=True)
    published = models.CharField(max_length=10, null=True, blank=True)
    pages = models.CharField(max_length=10, null=True, blank=True)
        
    def get_field_labels():
        return {
            'token': 'Tähis',
            'published': 'Kaitstud',
            'pages': 'Lehekülgi',
        }

    def get_label(self):
        return self.token + ' ' + self.published + ' ' + self.pages
    
    def __str__(self):
        return self.token + ' ' + self.published + ' ' + self.pages
