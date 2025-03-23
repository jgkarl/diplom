from django.contrib import admin
from ems.models import Keyword, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    
@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('id', 'field_001', 'field_148', 'field_150', 'field_151', 'field_155', 'field_670', 'field_680')