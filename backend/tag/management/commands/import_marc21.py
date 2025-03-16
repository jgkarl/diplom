import os
from django.core.management.base import BaseCommand
from pymarc import MARCReader, Record, Field
from tag.models import EmsKeyword, EmsCategory, EmsKeywordCategory
from pymarc import exceptions as exc
from django.db.models import Q

class Command(BaseCommand):
    help = 'Import MARC21 entries from a .mrc file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the .mrc file')
        parser.add_argument('--batch_size', type=int, default=100000, help='The number of records to process in one batch')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        batch_size = kwargs['batch_size']
        
        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f'File "{file_path}" does not exist'))
            return
        with open(file_path, 'rb') as fh:
            reader = MARCReader(fh, to_unicode=True, force_utf8=True)
            for i, record in enumerate(reader):
                if i >= batch_size:
                    break
                else:
                    self.stdout.write(self.style.SUCCESS(f'"{i}": "{record["001"].value()}"'))

                keyword, created = EmsKeyword.objects.get_or_create(field_001=record['001'].value())
                if not created:
                    self.stdout.write(self.style.WARNING(f'   INFO: Keyword with field_001 "{record["001"].value()}" already exists. Updating the existing record.'))
                
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
                
                if '450' in record:
                    for field in record.get_fields('450'):
                        is_english = field.indicator2 == '9'
                        synonym, created = keyword.synonyms.get_or_create(field_450=field['a'], is_english=is_english)
                
                if '451' in record:
                    for field in record.get_fields('451'):
                        is_english = field.indicator2 == '9'
                        synonym, created = keyword.synonyms.get_or_create(field_451=field['a'], is_english=is_english)
                
                if '455' in record:
                    for field in record.get_fields('455'):
                        is_english = field.indicator2 == '9'
                        synonym, created = keyword.synonyms.get_or_create(field_455=field['a'], is_english=is_english)

                if '550' in record:
                    for field in record.get_fields('550'):
                        relation_type = field['w'] if 'w' in field else 'x'
                        if '0' in field:
                            uri = field['0']
                            related_keyword_id = uri.split('/')[-1]
                            related_keyword, created = EmsKeyword.objects.get_or_create(field_001=related_keyword_id)
                            if created:
                                self.stdout.write(self.style.SUCCESS(f'SUCCESS: Created related keyword with field_001 "{related_keyword_id}"'))
                            relation, created = keyword.relations.get_or_create(related_keyword=related_keyword, relation_type=relation_type, via_field='550')
                        else:
                            related_keyword = None
                            self.stdout.write(self.style.WARNING(f'  > WARNING: Related keyword with field_001 "{related_keyword_id}" not found. Skipping relation.'))

                if '551' in record:
                    for field in record.get_fields('551'):
                        relation_type = field['w'] if 'w' in field else 'x'
                        if '0' in field:
                            uri = field['0']
                            related_keyword_id = uri.split('/')[-1]
                            related_keyword, created = EmsKeyword.objects.get_or_create(field_001=related_keyword_id)
                            if created:
                                self.stdout.write(self.style.SUCCESS(f'SUCCESS: Created related keyword with field_001 "{related_keyword_id}"'))
                            relation, created = keyword.relations.get_or_create(related_keyword=related_keyword, relation_type=relation_type, via_field='551')
                        else:
                            related_keyword = None
                            self.stdout.write(self.style.WARNING(f'  > WARNING: Related keyword with field_001 "{related_keyword_id}" not found. Skipping relation.'))

                if '555' in record:
                    for field in record.get_fields('555'):
                        relation_type = field['w'] if 'w' in field else 'x'
                        if '0' in field:
                            uri = field['0']
                            related_keyword_id = uri.split('/')[-1]
                            related_keyword, created = EmsKeyword.objects.get_or_create(field_001=related_keyword_id)
                            if created:
                                self.stdout.write(self.style.SUCCESS(f'SUCCESS: Created related keyword with field_001 "{related_keyword_id}"'))
                            relation, created = keyword.relations.get_or_create(related_keyword=related_keyword, relation_type=relation_type, via_field='555')
                        else:
                            related_keyword = None
                            self.stdout.write(self.style.WARNING(f'  > WARNING: Related keyword with field_001 "{related_keyword_id}" not found. Skipping relation.'))
                i += 1
                
                main_value = keyword.field_148 or keyword.field_150 or keyword.field_151 or keyword.field_155
                self.stdout.write(self.style.SUCCESS(f'SUCCESS: Imported keyword with field_001 "{keyword.field_001}" and main value "{main_value}"'))

        self.stdout.write(self.style.SUCCESS(f'Successfully imported first "{batch_size}" MARC21 entries'))
        
        # import is done, now give data about operation
        
        keywords_with_only_field_001 = EmsKeyword.objects.filter(
            Q(field_001__isnull=False) &
            Q(field_148__isnull=True) &
            Q(field_150__isnull=True) &
            Q(field_151__isnull=True) &
            Q(field_155__isnull=True) &
            Q(field_670__isnull=True) &
            Q(field_680__isnull=True)
        )
        
        self.stdout.write(self.style.SUCCESS(f'Keyword with only field_001: {keywords_with_only_field_001.count()}'))
        for i, keyword in enumerate(keywords_with_only_field_001):
            if i >= 5:
                break
            self.stdout.write(self.style.SUCCESS(f'Keyword ID: {keyword.id}, field_001: {keyword.field_001}'))