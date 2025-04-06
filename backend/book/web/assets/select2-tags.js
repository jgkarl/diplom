// Basic configuration for Select2 widget
function initializeSelect2(selector) {
    $(selector).select2({
        width: '100%', 
        placeholder: 'Search for books...', 
        allowClear: false, 
        minimumInputLength: 1,
        minimumResultsForSearch: 1, 
        data: [],
        ajax: {
            url: '/api/v1/tag/search',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    q: params.term 
                };
            },
            processResults: function(data) {
                return {
                    results: data.map(function(item) {
                        return {
                            id: item.id,
                            text: item.name
                        };
                    })
                };
            },
            cache: true
        },
        templateResult: function (data) {
            return data.text; // Format for displaying options
        },
    });
}

$(document).ready(function () {
    initializeSelect2('#search-bar');
});
