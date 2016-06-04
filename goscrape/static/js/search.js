function initSearch() {

    // selector cache
    var $kir = $('.ui.search');

    // mapping example
    $kir.search({
        type: 'category',
        minCharacters: 1,
        apiSettings: {
            onFailure: function (response) {
                console.log(response);
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
                        cat = item.category || 'Unkn own',
                        maxLength = 200
                        ;
                    if (index >= 10) {
                        // only show 8 results
                        return false;
                    }

                    // Create new language category
                    if (response.results[cat] === undefined) {
                        response.results[cat] = {
                            name: cat,
                            results: []
                        };
                    }

                    // Add result to category
                    response.results[cat].results.push({
                        title: item.name,
                        category: item.category,
                        icon: item.icon,
                        component: item.component
                    });
                });
                return response;
            },
            url: 'http://127.0.0.1:5000/search/app/{query}'
        },
        onSelect: function (item, response) {
            console.log(item)
            addFields(item.title, item.category, item.icon, item.component);
        }
    })
    ;


};


// attach ready event
$(document)
    .ready(initSearch)
;