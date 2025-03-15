import os
from django.core.management.base import BaseCommand
from pymarc import MARCReader, Record, Field
from tag.models import EmsKeyword, EmsCategory, EmsKeywordCategory
from pymarc import exceptions as exc

class Command(BaseCommand):
    help = 'Import MARC21 entries from a .mrc file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the .mrc file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return
        with open(file_path, 'rb') as fh:
            reader = MARCReader(fh, to_unicode=True, force_utf8=True)
            for i, record in enumerate(reader):
                if i >= 10000:
                    break
                keyword, created = EmsKeyword.objects.get_or_create(field_001=record['001'].value())
                if not created:
                    self.stdout.write(self.style.WARNING(f'>>> INFO: Keyword with field_001 "{record["001"].value()}" already exists. Updating the existing record.'))
                
                keyword.marc21 = record.as_json()
                keyword.field_001 = record['001'].value() if '001' in record else None
                keyword.field_148 = record['148']['a'] if '148' in record and 'a' in record['148'] else None
                keyword.field_150 = record['150']['a'] if '150' in record and 'a' in record['150'] else None
                keyword.field_151 = record['151']['a'] if '151' in record and 'a' in record['151'] else None
                keyword.field_155 = record['155']['a'] if '155' in record and 'a' in record['155'] else None
                keyword.field_670 = record['670']['a'] if '670' in record and 'a' in record['670'] else None
                keyword.field_680 = record['680']['i'] if '680' in record and 'i' in record['680'] else None
                
                keyword.save()
                
                if '072' in record:
                    for field in record.get_fields('072'):
                        category_code = field['a']
                        category, created = EmsCategory.objects.get_or_create(code=category_code)
                        
                        EmsKeywordCategory.objects.get_or_create(keyword=keyword, category=category)
                
                i += 1
                
                main_value = keyword.field_148 or keyword.field_150 or keyword.field_151 or keyword.field_155
                self.stdout.write(self.style.SUCCESS(f'SUCCESS: Imported keyword with field_001 "{keyword.field_001}" and main value "{main_value}"'))

        self.stdout.write(self.style.SUCCESS('Successfully imported first 10000 MARC21 entries'))
