from django_select2.forms import Select2TagWidget


class MySelect2TagWidget(Select2TagWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attrs["data-ajax--method"] = "GET"
        self.attrs["data-ajax--delay"] = 250
        self.attrs["data-ajax--cache"] = "true"
        self.attrs["data-ajax--dataType"] = "json"
        self.attrs["data-ajax--url"] = "/api/v1/tag/search"
        self.attrs["data-ajax--processResults"] =  (
            "function(data) {return {results: data.map(function(item) {return {id: item.id,text: item.name};})};},"
        )
