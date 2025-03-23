from django.core.management.base import BaseCommand
from ems.models import Keyword
from tag.models import Tag


class Command(BaseCommand):
    help = 'Transfer EMS Keywords to TAG app main model'

    def handle(self, *args, **kwargs):
        keywords = Keyword.objects.all()
        created_count = 0

        for keyword in keywords:
            external_id = getattr(keyword, 'field_001', None)
            name = (
                getattr(keyword, 'field_148', None) or
                getattr(keyword, 'field_150', None) or
                getattr(keyword, 'field_151', None) or
                getattr(keyword, 'field_155', None)
            )

            if external_id and name:
                Tag.objects.create(
                    external_id=external_id,
                    name=name
                )
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully transferred {created_count} keywords to TAG app main model.'))