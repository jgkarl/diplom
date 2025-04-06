from django import forms
from tag.models import Tag
from book.models import BookCategory, BookDepartment, BookLanguage, BookTag
from classifier.models import Item, Type
from django_select2.forms import Select2TagWidget
from book.widgets.widgets import MySelect2TagWidget
from book.models.Book import Book
from person.models import Person
from django.db import transaction
from core.helpers import get_superuser
import logging

logger = logging.getLogger(__name__)


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        labels = Book.get_field_labels()

    exclude = [
        "uuid",
        "version",
        "active",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "deleted_at",
        "deleted_by",
    ]
    readonly_fields = ["status"]

    active = forms.BooleanField(
        label=Meta.labels["active"],
        required=False,
    )

    token = forms.CharField(
        widget=forms.TextInput(attrs={"style": "width: 100%;"}),
        max_length=64,
        label=Meta.labels["token"],
        required=False,
    )

    published = forms.CharField(
        widget=forms.TextInput(attrs={"style": "width: 100%;"}),
        max_length=10,
        label=Meta.labels["published"],
        required=False,
    )

    pages = forms.CharField(
        widget=forms.TextInput(attrs={"style": "width: 100%;"}),
        max_length=10,
        label=Meta.labels["pages"],
        required=False,
    )

    format = forms.ModelChoiceField(
        widget=forms.Select(attrs={"style": "width: 100%;"}),
        queryset=Item.objects.filter(type__identifier="book_format"),
        required=False,
    )

    status = forms.ModelChoiceField(
        widget=forms.Select(attrs={"style": "width: 100%;"}),
        queryset=Item.objects.filter(type__identifier="book_status"),
        label=Meta.labels["status"],
        required=True,
    )

    notes = forms.CharField(
        widget=forms.Textarea(attrs={"style": "width: 100%;", "rows": 3}),
        label=Meta.labels["notes"],
        required=False,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        widget=MySelect2TagWidget(),
        label=Meta.labels["tags"],
        required=False,
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={"style": "width: 100%;", "data-tags": "false"}),
        label=Meta.labels["categories"],
        required=False,
    )

    departments = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={"style": "width: 100%;", "data-tags": "false"}),
        label=Meta.labels["departments"],
        required=False,
    )

    languages = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={"style": "width: 100%;"}),
        label=Meta.labels["languages"],
        required=False,
    )

    authors = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=Select2TagWidget(attrs={"style": "width: 100%;"}),
        label=Meta.labels["authors"],
        required=False,
    )

    supervisors = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=Select2TagWidget(attrs={"style": "width: 100%;"}),
        label=Meta.labels["supervisors"],
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs.update(
            {
                "style": "width: 100%;",
            }
        )
        
        self.fields["categories"].queryset = Item.objects.filter(
            type__identifier="book_category"
        )
        self.fields["departments"].queryset = Item.objects.filter(
            type__identifier="book_department"
        )
        self.fields["languages"].queryset = Item.objects.filter(
            type__identifier="language"
        )
        self.fields["authors"].queryset = Person.objects.all()
        self.fields["supervisors"].queryset = Person.objects.all()

        if self.instance and self.instance.pk:
            self.fields["tags"].initial = self.instance.tag_items()
            self.fields["categories"].initial = self.instance.category_items()
            self.fields["departments"].initial = self.instance.department_items()
            self.fields["languages"].initial = self.instance.language_items()
            self.fields["authors"].initial = self.instance.get_authors()
            self.fields["supervisors"].initial = self.instance.get_supervisors()

    def save(self, commit=True):
        try:
            with transaction.atomic():
                instance = super(BookForm, self).save(commit=False)

                if "tags" in self.cleaned_data:
                    self.save_tags(instance, self.cleaned_data["tags"])
                if "categories" in self.cleaned_data:
                    self.save_categories(instance, self.cleaned_data["categories"])
                if "departments" in self.cleaned_data:
                    self.save_departments(instance, self.cleaned_data["departments"])
                if "languages" in self.cleaned_data:
                    self.save_languages(instance, self.cleaned_data["languages"])
                if "authors" in self.cleaned_data:
                    self.save_persons(instance, self.cleaned_data["authors"], "author")
                if "supervisors" in self.cleaned_data:
                    self.save_persons(
                        instance, self.cleaned_data["supervisors"], "supervisor"
                    )

                return instance
        except Exception as e:
            transaction.rollback()
            raise e

    def save_tags(self, instance, tags):
        instance.book_tags.all().delete()
        for tag in tags:
            book_tag = BookTag.objects.create(
                book=instance, tag=tag, created_by=get_superuser()
            )
            instance.book_tags.add(book_tag)

    def save_categories(self, instance, categories):
        instance.book_categories.all().delete()
        for category in categories:
            book_category = BookCategory.objects.create(
                book=instance, type=category, created_by=get_superuser()
            )
            instance.book_categories.add(book_category)

    def save_departments(self, instance, departments):
        instance.book_departments.all().delete()
        for department in departments:
            book_department = BookDepartment.objects.create(
                book=instance, type=department, created_by=get_superuser()
            )
            instance.book_departments.add(book_department)

    def save_languages(self, instance, languages):
        instance.book_languages.all().delete()
        for language in languages:
            # if not isinstance(language, Item):
            #     language, created = Item.objects.get_or_create(
            #         name=language,
            #         type=Type.objects.get(identifier="language"),
            #         defaults={"created_by": get_superuser()},
            #     )
            book_language = BookLanguage.objects.create(
                book=instance, type=language, created_by=get_superuser()
            )
            instance.book_languages.add(book_language)

    def save_persons(self, instance, persons, relation):
        instance.book_persons.filter(relation__name_en=relation).delete()
        for person in persons:
            instance.book_persons.create(
                person=person,
                relation=Item.objects.get(name_en=relation),
                created_by=get_superuser(),
            )
