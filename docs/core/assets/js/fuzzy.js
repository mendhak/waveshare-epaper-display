
const fuzzy = {
    autocomplete: {},
    el: {
        searchInput: document.querySelector('#searchInput'),
        searchInputAlt: document.querySelector('#searchInputAlt')
    },
    initAutocompletes: function() {
        const elsInput = [fuzzy.el.searchInput, fuzzy.el.searchInputAlt];
        elsInput.forEach(function(elInput) {
            if (elInput !== null) {
                elInput.addEventListener('keydown', fuzzy.handlers._keyDown);
                const inputId = elInput.id;
                fuzzy.autocomplete[inputId] = new Autocomplete(inputId, {
                    clearButton: false,
                    onSearch: ({ currentValue }) => {
                        // local data
                        const fuseOptions = {
                            includeScore: true,
                            includeMatches: true,
                            keys: ['url', 'title', 'description']
                        }
                        const fuse = new Fuse(fuzzy.sanitizedIndex, fuseOptions);
                        const fuseResult = fuse.search(currentValue);
                        return fuseResult;
                    },

                    onResults: ({ matches }) => {
                        return matches
                            .map((el) => {
                                let description = '';
                                if (el.item.description.trim().length > 0) description = `<span>${el.item.description}</span>`;
                                return `<li>${el.item.title} ${description}</li>`;
                            })
                            .join('');
                    },
                
                    onSubmit: ({index, element, object, results}) => {
                        // console.log('onSubmit: ', index, element, object, results);
                        location.href = object.item.url;
                    }
                });
            }
        });
    },
    initIndex: function(evt) {
        if (fuzzy.indexItems === null && typeof libdocSystem.fuzzyIndexUrl == 'string') {
            const fuzzyIndex = fuzzy.getJson(libdocSystem.fuzzyIndexUrl);
            fuzzyIndex.then(jsonFetch => {
                fuzzy.indexItems = jsonFetch;
                fuzzy.sanitizeIndex();
                evt.target.removeEventListener('focus', fuzzy.handlers._focusInput);
                // console.log(`event listener ${evt.target.id} removed and index OK`, fuzzy.indexItems);
                fuzzy.initAutocompletes();
            });
        }
    },
    handlers: {
        _focusInput: function(evt) {
            fuzzy.initIndex(evt);
        },
        _keyDown: function(evt) {
            if (evt.keyCode === 13) {
                evt.target.form.submit();
            }
        }
    },
    getJson: async function(url) {
        try {
            const response = await fetch(url);
            const data = await response.json();
            return data;
        } catch (error) {
            console.log(error);
            return [];
        }
    },
    sanitizeIndex: function() {
        if (typeof fuzzy.indexItems !== null && fuzzy.sanitizedIndex === null) {
            const filterArray = [];
            fuzzy.sanitizedIndex = [];
            fuzzy.indexItems.forEach(function(item) {
                if (!filterArray.includes(item.title)) {
                    let canBePushed = true;
                    switch (item.title) {
                        case './core/libdoc_blog.liquid':
                            item.title = libdocConfig.blogTitle;
                            item.description = libdocConfig.blogDescription === 'false' ? '' : libdocConfig.blogDescription;
                            if (!libdocSystem.blogPostsCount) canBePushed = false;
                            break;
                        case './core/libdoc_tags.liquid':
                            item.title = libdocMessages.tagsList;
                            item.description = libdocMessages.tagsListDescription;
                            if (!libdocConfig.displayTagsListLink) canBePushed = false;
                            break;
                        default:
                            break;
                    }
                    if (canBePushed) fuzzy.sanitizedIndex.push(item);
                    
                }
            });
        }
    },
    sanitizedIndex: null,
    indexItems: null,
    update: function() {
        if (typeof Fuse == 'function' && typeof libdocSystem.searchIndexUrl == 'string') {
            if (fuzzy.el.searchInput !== null) {
                fuzzy.el.searchInput.addEventListener('focus', fuzzy.handlers._focusInput);
            };
            if (fuzzy.el.searchInputAlt !== null) {
                fuzzy.el.searchInputAlt.addEventListener('focus', fuzzy.handlers._focusInput);
            };
        }
    }
}
document.addEventListener('DOMContentLoaded', fuzzy.update);
