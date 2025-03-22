from django.contrib import admin
from django.db import models
from core.models.abstract import AuditableModel, AuditableAdmin, AuditableModelResource

class Person(AuditableModel):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=False)
    birth = models.CharField(max_length=10, null=True)
    death = models.CharField(max_length=10, null=True)
    notes = models.TextField()
    
    def fullname(self):
        parts = [self.first_name, self.last_name]
        return ' '.join(part for part in parts if part)
    
    def get_field_labels():
        return {
            'first_name': 'Eesnimi',
            'last_name': 'Perekonnanimi',
            'birth': 'Sünd',
            'death': 'Surm',
            'notes': 'Märkmed',
        }
        
    def get_label(self):
        return self.fullname()
    
    def __str__(self):
        return self.fullname()

class PersonResource(AuditableModelResource):
    class Meta:
        model = Person
        fields = ('id', 'first_name', 'last_name')
        export_order = ('first_name', 'last_name', 'birth', 'death', 'notes')

@admin.register(Person)
class PersonAdmin(AuditableAdmin):
    list_display = ['fullname', 'first_name', 'last_name', 'active']
    search_fields = ['first_name', 'last_name']
    list_filter = ['active']
    resource_class = PersonResource