
const search = {
    el: {
        searchInput: document.querySelector('#searchInput'),
        searchResults: document.querySelector('#searchResults'),
        pageH1: document.querySelector('h1')
    },
    decodeHtmlCharCodes: function(str) { 
        // https://stackoverflow.com/a/54346501
        return str.replace(/(&#(\d+);)/g, function(match, capture, charCode) {
            return String.fromCharCode(charCode);
        });
    },
    sanitizeQuery: function(queryString) {
        return queryString.replaceAll('\\', '');
    },
    HTMLEncode: function(str) {
        // https://stackoverflow.com/a/784765
        str = [...str];
        //    ^ es20XX spread to Array: keeps surrogate pairs
        let i = str.length, aRet = [];
      
        while (i--) {
            var iC = str[i].codePointAt(0);
            if (iC < 65 || iC > 127 || (iC>90 && iC<97)) {
                aRet[i] = '&#'+iC+';';
            } else {
                aRet[i] = str[i];
            }
        }
        return aRet.join('');
    },
    searchIndex: function(query) {
        if (typeof search.searchIndexArray == 'object' && search.searchIndexArray !== null) {
            let markup = '';
            const itemTitleIgnoreFilter = [];
            search.searchIndexArray.forEach(function(item) {
                if (!itemTitleIgnoreFilter.includes(item.title)) {
                    query = search.sanitizeQuery(query);
                    const   itemContent = `${item.content} ${item.title}`,
                            content = search.decodeHtmlCharCodes(itemContent).toLowerCase(),
                            queryLowered = query.toLowerCase(),
                            queryLoweredEncoded = search.HTMLEncode(queryLowered),
                            occurrenceIndex = content.indexOf(queryLowered),
                            range = 200,
                            resultUrl = `${item.url}?text=${encodeURIComponent(query)}`;
                    let lowIndex = occurrenceIndex - range,
                        highIndex = occurrenceIndex + query.length + range;
                    if (lowIndex < 0) lowIndex = 0;
                    if (highIndex > content.length - 1) highIndex = content.length - 1;
                    let summary = content.slice(lowIndex, highIndex);
                    summary = search.HTMLEncode(summary);
                    summary = summary.replaceAll(queryLoweredEncoded, ` <mark class="fvs-wght-600 wb-break-all">${query}</mark> `);
                    if (resultUrl.indexOf('/tags/?') === 0) item.title = libdocMessages.tagsList;
                    if (content.indexOf(queryLowered) > -1) {
                        markup += search.renderSearchResult({url: resultUrl, title: item.title, summary: summary})
                    }
                }
            });
            search.el.pageH1.innerHTML += `<mark class="fvs-wght-600 wb-break-all">${query}</mark>`;
            if (markup == '') {
                search.el.searchResults.innerHTML = `<li>${libdocMessages.searchResultsNoResultForQuery} <mark class="fvs-wght-600 wb-break-all">${query}</mark></li>`;
            } else {
                search.el.searchResults.innerHTML = markup;
            }
            search.el.searchInput.value = query;
        }
    },
    renderSearchResult: function({url, title, summary}) {
        return `
            <li class="d-flex fd-column gap-2 | pb-5">
                <a  href="${url}"
                    class="fvs-wght-600 fs-5">
                    ${title}
                </a>
                <div class="wb-break-all fs-4" fs-3="xs">
                    ${summary}
                </div>
            </li>
        `;
    },
    renderLoadingResults: function() {
        const item = `
            <li class="d-flex fd-column pb-5">
                <a  href="#!">
                    <span class="d-flex | p-2 | bc-primary-300 brad-3 | __anim-blink"></span>
                </a>
                <div class="d-flex | mt-3 p-1 | bc-neutral-300 brad-3 | __anim-blink"></div>
                <div class="d-flex | mt-1 p-1 | bc-neutral-300 brad-3 | __anim-blink"></div>
                <div class="d-flex | mt-1 p-1 | bc-neutral-300 brad-3 | __anim-blink"></div>
            </li>`;
        let markup = '';
        for (let i = 0; i < 3; i++) markup += item;
        return markup;
    },
    searchIndexArray: null,
    getUrlSearchParams: function() {
        return new URLSearchParams(location.search).get('search');
    },
    search: function(query) {
        if (typeof query == 'string'
            && search.searchIndexArray !== null
            && typeof search.searchIndexArray == 'object') {
            if (query.length > 0) {
                query = search.sanitizeQuery(query);
                search.searchIndex(query);
            }
        }
    },
    sanitizeIndex: function() {
        if (typeof search.searchIndexArray !== null) {
            search.searchIndexArray.forEach(function(item) {
                switch (item.title) {
                    case './core/libdoc_blog.liquid':
                        item.title = libdocConfig.blogTitle
                        break;

                    case './core/libdoc_tags.liquid':
                        item.title = libdocMessages.tagsList;
                        break;
                
                    default:
                        break;
                }
            })
        }
    },
    update: function() {
        const query = search.getUrlSearchParams();
        if (typeof libdocSystem.searchIndexUrl == 'string'
            && search.el.searchInput !== null
            && search.el.searchResults !== null
            && search.el.pageH1 !== null
        ) {
            if (query !== null) search.el.searchResults.innerHTML = search.renderLoadingResults();
            fetch(libdocSystem.searchIndexUrl)
                .then(response => response.json())
                .then(searchIndexArray => {
                    search.searchIndexArray = searchIndexArray;
                    search.sanitizeIndex();
                    if (query !== null) search.search(query);
                })
                .catch(error => {
                    // Handle the error
                    console.log(error);
                });
        }
    }
}
document.addEventListener('DOMContentLoaded', search.update);
