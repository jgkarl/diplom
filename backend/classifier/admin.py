from django.contrib import admin
from django.utils import timezone
from django.utils.http import urlencode
from django.utils.html import format_html
from django.urls import reverse
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from core.helpers import snake_to_sentence, get_superuser
from .models import Type, Item

# Register your models here.

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_filter = ['active']
    list_display = ['name', 'name_en', 'active', 'item_count', 'view_items_link']
    search_fields = ['name', 'name_en']
    
    def item_count(self, obj):
        return obj.classifier_type_items.count()
    
    def view_items_link(self, obj):
        count = obj.classifier_type_items.count()
        url = (
            reverse("admin:classifier_item_changelist")
            + "?"
            + urlencode({"type__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Items</a>', url, count)

    view_items_link.short_description = "Items"

class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        exclude = ('code', 'position', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by')

    def before_import_row(self, row, **kwargs):
        type_input = row.get('type')
        if type_input:
            try:
                if isinstance(type_input, int):
                    type_instance = Type.objects.get(id=type_input)
                else:
                    type_instance = Type.objects.get(identifier=type_input)
            except Type.DoesNotExist:
                type_instance = Type.objects.create(identifier=type_input, name=snake_to_sentence(type_input))
            row['type'] = type_instance.id
    
    def before_save_instance(self, instance, row, **kwargs):
        superuser = get_superuser()
        instance.created_by = superuser if superuser else None

@admin.register(Item)
class ItemAdmin(ImportExportActionModelAdmin):
    list_editable = ['active']
    list_filter = ['active', 'type']
    list_display = ['name', 'name_en', 'active', 'typename_link', 'code']
    search_fields = ['name', 'name_en', 'code']
    readonly_fields = ['code', 'position']
    
    resource_class = ItemResource
    
    # Custom field to display the related type
    def typename_link(self, obj):
        url = reverse("admin:classifier_type_change", args=[obj.type.id])
        return format_html('<a href="{}">{}</a>', url, obj.type.name)
    
    typename_link.short_description = "Classifier Type"

    # Exclude fields from the form based on user permissions
    exclude = ['created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by']
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:
            exclude.append(['active', 'code', 'position', 'type'])
        return exclude
    
    # Apply automatic timestamp and behavioural fields for base CRUD operations
    # TODO: write into custom reusable mixin behaviour
    def save_model(self, request, obj, form, change):
        if not change:  # Object is being created
            obj.created_at = timezone.now()
            obj.created_by = request.user
        obj.updated_at = timezone.now()
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.deleted_at = timezone.now()
        obj.deleted_by = request.user
        obj.save()

    # Custom actions for bulk operations
    def deactivate(self, request, queryset):
        queryset.update(active=False)
    
    def activate(self, request, queryset):
        queryset.update(active=True)
    
    actions = ['activate','deactivate','delete_selected']