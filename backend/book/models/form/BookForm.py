from django import forms
from classifier.models import Item
from django_select2.forms import Select2TagWidget
from book.models.Book import Book
from person.models import Person

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        labels = Book.get_field_labels()
    
    exclude = ['uuid', 'version', 'active', 'created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at', 'deleted_by']
    readonly_fields = ['status']

    token = forms.CharField(max_length=64, label=Meta.labels['token'], required=False)
    published = forms.CharField(max_length=10, label=Meta.labels['published'], required=False)

    notes = forms.CharField(
        widget=forms.Textarea(attrs={"cols": 80, "rows": 3}),
        label=Meta.labels['notes'],
        required=False
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={'style': 'width: 100%;'}),
        required=False
    )
    departments = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={'style': 'width: 100%;'}),
        required=False
    )
    languages = forms.ModelMultipleChoiceField(
        queryset=Item.objects.none(),
        widget=Select2TagWidget(attrs={'style': 'width: 100%;'}),
        required=False
    )
    authors = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=Select2TagWidget(attrs={'style': 'width: 100%;'}),
        required=False,
    )
    supervisors = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=Select2TagWidget(attrs={'style': 'width: 100%;'}),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['categories'].queryset = Item.objects.filter(type__identifier='book_category')
        self.fields['departments'].queryset = Item.objects.filter(type__identifier='book_department')
        self.fields['languages'].queryset = Item.objects.filter(type__identifier='language')
        self.fields['authors'].queryset = Person.objects.all()
        self.fields['supervisors'].queryset = Person.objects.all()

        if self.instance and self.instance.pk:
            self.fields['categories'].initial = self.instance.category_items()
            self.fields['departments'].initial = self.instance.department_items()
            self.fields['languages'].initial = self.instance.language_items()
            self.fields['authors'].initial = self.instance.get_authors()
            self.fields['supervisors'].initial = self.instance.get_supervisors()
