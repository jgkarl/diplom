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
            url: '/api/v1/select2',
            dataType: 'json',
            delay: 250,
            cache: true,
            data: function(params) {
                return {
                    q: params.term 
                };
            },
            processResults: function(data) {
                return {
                    results: data
                };
            },
        },
    });
}

$(document).ready(function () {
    initializeSelect2('#search-bar');
});
