function initSearch() {

    // selector cache
    var $kir = $('.ui.search');

    // mapping example
    $kir.search({
        type: 'category',
        minCharacters: 1,
        apiSettings: {
            onFailure: function () {
                $(this).search('display message', '<b>Hold off a few minutes</b> <div class="ui divider"></div> GitHub rate limit exceeded for anonymous search.');
            },
            onResponse: function (githubResponse) {
                var
                    response = {
                        results: {}
                    }
                    ;
                if (githubResponse.items.length === 0) {
                    // no results
                    return response;
                }
                $.each(githubResponse.items, function (index, item) {
                    var
                        language = item.language || 'Unknown',
                        maxLength = 200,
                        description
                        ;
                    if (index >= 5) {
                        // only show 8 results
                        return false;
                    }
                    // Create new language category
                    if (response.results[language] === undefined) {
                        response.results[language] = {
                            name: language,
                            results: []
                        };
                    }
                    description = (item.description < maxLength)
                        ? item.description
                        : item.description.substr(0, maxLength) + '...'
                    ;
                    description = $.fn.search.settings.templates.escape(description);
                    // Add result to category
                    response.results[language].results.push({
                        title: item.name,
                        description: description
                    });
                });
                return response;
            },
            url: 'https://api.github.com/search/repositories?q={query}'
        },
        onSelect: function (kir, kiri) {
            console.log(kir.title);
            console.log(kiri);
            addFields(kir.title);
        }
    })
    ;


};


// attach ready event
$(document)
    .ready(initSearch)
;
