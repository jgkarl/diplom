from django.db import models
from core.models.abstract import AuditableModel
from django.utils.translation import gettext_lazy as _

import logging
logger = logging.getLogger(__name__)

class Book(AuditableModel):
    token = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Token'))
    published = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Published'))
    pages = models.CharField(max_length=10, null=True, blank=True, verbose_name=_('Pages'))
    
    format = models.ForeignKey('classifier.Item', related_name='book_formats', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'book_format'}, null=True, verbose_name=_('Format'))
    status = models.ForeignKey('classifier.Item', related_name='book_statuses', on_delete=models.DO_NOTHING, limit_choices_to={'type__identifier': 'book_status'}, null=False, verbose_name=_('Status'))
    
    notes = models.TextField(null=True, blank=True, verbose_name=_('Notes'))

    def get_field_labels():
        labels = {
            'categories': _('Categories'),
            'departments': _('Departments'),
            'languages': _('Languages'),
            'authors': _('Authors'),
            'supervisors': _('Supervisors'),
        }
        
        labels.update({field.name: field.verbose_name for field in Book._meta.fields})
        logger.debug(f"Labels: {labels}")
        return labels

    def category_items(self):
        return list(self.book_categories.values_list('type_id', flat=True))
        
    def department_items(self):
        return list(self.book_departments.values_list('type_id', flat=True))
    
    def language_items(self):
        return list(self.book_languages.values_list('type_id', flat=True))

    def get_authors(self):
        return self.book_persons.filter(relation__name_en='author').values_list('person_id', flat=True)
    
    def authors(self):
        return list(map(lambda x: x.person.fullname(), self.book_persons.filter(relation__name_en='author').all()))
    
    def get_supervisors(self):
        return self.book_persons.filter(relation__name_en='supervisor').values_list('person_id', flat=True)

    def supervisors(self):
        return list(map(lambda x: x.person.fullname(), self.book_persons.filter(relation__name_en='supervisor').all()))

    def get_department(self):
        return self.book_departments.first()
    
    # model general getters
    def get_label(self):
        return self.book_names.first().name if self.book_names.first() else 'No name' 
        
    def __str__(self):
        return self.uuid.__str__()
