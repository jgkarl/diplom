from django.db import models
from uuid import uuid4

class EmsCategory(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    code = models.CharField(max_length=255, unique=True, null=False)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.uuid.__str__()

class EmsKeyword(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    marc21 = models.JSONField(null=True)
    field_001 = models.CharField(max_length=255, unique=True, null=False)
    field_148 = models.TextField(null=True)
    field_150 = models.TextField(null=True)
    field_151 = models.TextField(null=True)
    field_155 = models.TextField(null=True)
    field_670 = models.TextField(null=True)
    field_680 = models.TextField(null=True)

    def __str__(self):
        return self.uuid.__str__()

class EmsKeywordCategory(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(EmsKeyword, related_name='categories', on_delete=models.CASCADE)
    category = models.ForeignKey(EmsCategory, related_name='keywords', on_delete=models.CASCADE)

    def __str__(self):
        return self.uuid.__str__()
    
class EmsKeywordSynonym(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(EmsKeyword, related_name='synonyms', on_delete=models.CASCADE)
    field_450 = models.TextField(null=True)
    field_451 = models.TextField(null=True)
    field_455 = models.TextField(null=True)
    is_english = models.BooleanField(default=False)

    def __str__(self):
        return self.uuid.__str__()
    
class EmsKeywordRelation(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False, null=False)
    keyword = models.ForeignKey(EmsKeyword, related_name='relations', on_delete=models.CASCADE)
    related_keyword = models.ForeignKey(EmsKeyword, related_name='related_to', on_delete=models.CASCADE)
    via_field = models.TextField(null=True)
    relation_type = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.uuid.__str__()