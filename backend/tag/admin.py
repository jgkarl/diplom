from django.contrib import admin
from tag.models import Tag
from django.utils.html import format_html


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    readonly_fields = ("uuid", "external_id_link", "name")
    exclude = ("external_id",)

    def external_id_link(self, obj):
        if obj.external_id:
            return format_html(
                '<a href="https://www.ems.ee/{}" target="_blank">{}</a>',
                obj.external_id,
                obj.external_id,
            )
        return "-"

    external_id_link.short_description = "External ID Link"
    external_id_link.admin_order_field = "external_id"

    list_display = ("uuid", "external_id_link")

    class Meta:
        model = Tag
