from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    code = models.CharField(max_length=255, unique=True, null=False, verbose_name=_('Code'))
    name = models.CharField(max_length=255, null=True, verbose_name=_('Name'))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categorys')
      
    def __str__(self):
        return self.uuid.__str__()

class Keyword(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    marc21 = models.JSONField(null=True)
    field_001 = models.CharField(max_length=255, unique=True, null=False, verbose_name=_('EMS ID'))
    field_148 = models.TextField(null=True, verbose_name=_('Chronological term'))
    field_150 = models.TextField(null=True, verbose_name=_('Topical term'))
    field_151 = models.TextField(null=True, verbose_name=_('Geographic term'))
    field_155 = models.TextField(null=True, verbose_name=_('Form term'))
    field_670 = models.TextField(null=True, verbose_name=_('Source data'))
    field_680 = models.TextField(null=True, verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Keyword')
        verbose_name_plural = _('Keywords')
      
    def __str__(self):
        return self.uuid.__str__()

class KeywordCategory(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(Keyword, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='keywords', on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid.__str__()
    
class KeywordSynonym(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(Keyword, related_name='synonyms', on_delete=models.CASCADE)
    field_450 = models.TextField(null=True, verbose_name=_('Topical term'))
    field_451 = models.TextField(null=True, verbose_name=_('Geographic name'))
    field_455 = models.TextField(null=True, verbose_name=_('Form term'))
    is_english = models.BooleanField(default=False)

    def __str__(self):
        return self.uuid.__str__()
    
class KeywordRelation(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(Keyword, related_name='relations', on_delete=models.CASCADE)
    related_keyword = models.ForeignKey(Keyword, related_name='related_to', on_delete=models.CASCADE)
    via_field = models.TextField(null=True)
    relation_type = models.CharField(max_length=255, null=False, verbose_name=_('Relation type'))

    def __str__(self):
        return self.uuid.__str__()