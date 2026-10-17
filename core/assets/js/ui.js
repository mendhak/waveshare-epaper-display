const libdocUi = {
    defaults: {
        localStorageIdentifier: 'eleventyLibdoc',
        colorSchemes: ['auto', 'light', 'dark'],
        darkModeCssFilePath: `${libdocConfig.htmlBasePathPrefix}/core/assets/css/ds__dark_mode.css`,
        supportedLanguagesJsonPath: `${libdocConfig.htmlBasePathPrefix}/core/assets/js/supported-languages.json`,
        darkModeCssMedia: '',
        screenSizes: {
            xs: [0, 599],
            sm: [600, 959],
            md: [960, Infinity]
        },
    },
    userPreferences: {
        FTOCNormallyOpened: false,
        navPrimaryAccordion: 'pages'
    },
    el: {
        tocMain: document.querySelector('#toc_main'),
        tocMainOl: document.querySelector('#toc_main > ol'),
        navSmallDevicesFTOCBtn: document.querySelector('#sd_floating_toc_toggle_btn'),
        navSmallDevicesGTTBtn: document.querySelector('#sd_gtt_btn'),
        main: document.querySelector('main'),
        mainHeader: document.querySelector('main > header'),
        navPrimary: document.querySelector('#nav_primary'),
        navPrimaryCheckbox: document.querySelector('#nav_primary_checkbox'),
        navPrimaryContainer: document.querySelector('#nav_primary_container'),
        navSmallDevices: document.querySelector('#nav_small_devices'),
        searchForms: document.querySelectorAll('.search_form'),
        searchInputs: document.querySelectorAll('input[type="search"][name="search"]'),
        searchClearBtns: document.querySelectorAll('.search_form__clear_btn'),
        ftocHeadings: [],
        darkModeCssMetaLink: document.head.querySelector('#libdoc_dark_mode_css'),
        inputsColorScheme: document.querySelectorAll('[name="libdoc_color_scheme"]'),
        customLinks: document.querySelector('#custom_links')
    },
    getTransferSize: function() {
        // https://jmperezperez.com/blog/page-load-footer/
        let result = 0;
        if (typeof performance == 'object') {
            result = performance.getEntriesByType('resource').reduce((a, r) => {
                return a + r.transferSize;
            }, 0);
            result = Math.round(result / 1024);
        }
        return result;
    },
    getCurrentScreenSizeName: function() {
        let response = '';
        Object.keys(libdocUi.defaults.screenSizes).forEach(function(name) {
            const currentSizeName = libdocUi.defaults.screenSizes[name];
            if (window.innerWidth >= currentSizeName[0] && window.innerWidth <= currentSizeName[1]) {
                response = name;
            }
        });
        return response;
    },
    localStorageAvailable: function() {
        let storage;
        try {
            storage = window['localStorage'];
            const x = "__storage_test__";
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        } catch (e) {
            return (
                e instanceof DOMException &&
                // everything except Firefox
                (e.code === 22 ||
                    // Firefox
                    e.code === 1014 ||
                    // test name field too, because code might not be present
                    // everything except Firefox
                    e.name === "QuotaExceededError" ||
                    // Firefox
                    e.name === "NS_ERROR_DOM_QUOTA_REACHED") &&
                // acknowledge QuotaExceededError only if there's something already stored
                storage &&
                storage.length !== 0
            );
        }
    },
    // Get local storage data from identifier
    getLocalStorage: function(identifier) {
        if (libdocUi.localStorageAvailable() && typeof identifier == 'string') {
            return JSON.parse(localStorage.getItem(identifier));
        }
    },
    // Store on localStorage
    saveLocalStorage: function({identifier, backup}) {
        if (libdocUi.localStorageAvailable()
            && typeof identifier == 'string'
            && typeof backup == 'object') {
            // console.log('save', identifier, JSON.stringify(backup));
            localStorage.setItem(identifier, JSON.stringify(backup));
        }
    },
    // Clear localStorage
    clearLocalStorage: function(identifier) {
        if (libdocUi.localStorageAvailable()) {
            localStorage.removeItem(identifier);
        }
    },
    copyToClipboard: function(textToCopy, options) {
        const params = {
            notificationEnabled: function(value) {
                let result = typeof value == 'boolean' ? value : true;
                if (typeof value == 'string') {
                    if (value.toLocaleLowerCase() === 'false') result = false;
                }
                return result;
            },
            notificationContent: function(value) {
                return typeof value == 'string' ? value : libdocMessages.copyToClipboard;
            }
        }
        const userParams = {
            notificationEnabled: params.notificationEnabled(),
            notificationContent: params.notificationContent()
        }
        if (typeof options == 'object') {
            Object.keys(options).forEach(function(optionName) {
                if (typeof params[optionName] == 'function') {
                    const optionValue = options[optionName];
                    userParams[optionName] = params[optionName](optionValue);
                }
            });
        }
        if (navigator.clipboard !== undefined) {
            navigator.clipboard.writeText(textToCopy).then(
                function() {
                  /* clipboard successfully set */
                  if (userParams.notificationEnabled) libdocUi.notifications.add(userParams.notificationContent);
                }
            )
        } else {
            /* clipboard write failed */
            // Create a "hidden" input
            const aux = document.createElement("input");
            // Assign it the value of the specified element
            aux.setAttribute("value", textToCopy);
            // Append it to the body
            document.body.appendChild(aux);
            // Highlight its content
            aux.select();
            // Copy the highlighted text
            document.execCommand("copy");
            // Remove it from the body
            document.body.removeChild(aux);
            if (userParams.notificationEnabled) libdocUi.notifications.add(userParams.notificationContent);
        }
    },
    notifications: {
        defaults: {
            template: 'base',
            duration: 3,
            skin: 'primary'
        },
        templates: {
            base: function({id, message, duration, skin}) {
                return `
                    <aside class="
                        d-flex jc-space-between
                        pos-fixed z-3 top-0 right-0
                        mt-5 mr-5
                        bc-${skin}-100 c-${skin}-800 brad-2 bs-1"
                        mt-3="xs,sm"
                        mr-3="xs,sm"
                        id="${id}">
                        <div class="d-flex p-2">
                            <div class="pl-1 brad-3" style="background-color: yellowgreen"></div>
                        </div>
                        <div class="d-flex ai-center | pt-4 pb-4 pl-4 pr-7">
                            ${message}
                        </div>
                        <button class="
                            d-flex ai-center
                            pt-2 pb-2 pl-3 pr-3
                            fs-1 tt-uppercase
                            blwidth-1 blstyle-solid bcolor-neutral-700 c-${skin}-700 bc-${skin}-200 b-0 bradtr-2 bradbr-2
                            cur-pointer"
                            p-3="xs"
                            onclick="this.closest('aside').remove();">
                            ok
                        </button>
                        <style>
                            @keyframes ${id} {
                                100% {
                                    transform: translateY(-200%);
                                    opacity: 0;
                                    pointer-events: none;
                                }
                            }
                            #${id} {
                                animation: ${id} 500ms ${duration}s forwards;
                            }
                            #${id}:hover {
                                animation-play-state: paused;
                            }
                        </style>
                    </aside>
                `;
            }
        },
        add: function(message, options) {
            let n_tpl = this.defaults.template;
            let n_duration = this.defaults.duration;
            let n_skin = this.defaults.skin;
            if (typeof options == 'object') {
                // Template
                const custom_tpl = options.template;
                if (typeof custom_tpl == 'string') {
                    if (typeof this.templates[custom_tpl] == 'function') {
                        n_tpl = custom_tpl;
                    }
                }
                // Duration
                const custom_duration = options.duration;
                if (typeof custom_duration == 'number') {
                    n_duration = custom_duration;
                }
                // Color family name
                const custom_skin = options.skin;
                if (typeof custom_skin == 'string') {
                    n_skin = custom_skin;
                }

            }
            const n_id = 'notification_' + Date.now().toString();
            const n_markup = this.templates[n_tpl]({message: message, id: n_id, duration: n_duration, skin: n_skin});
            document.body.insertAdjacentHTML('beforeend', n_markup);
        }
    },
    handlers: {
        _colorSchemeClick: function(event) {
            // console.log(event.target.value)
            libdocUi.setColorScheme(event.target.value);
        },
        _touchStart: function(evt) {
            document.body.classList.add('touch-device');
            document.body.removeEventListener('touch', libdocUi.handlers._touchStart);
        },
        _clickCopyCodeBlock: function(evt) {
            const elBtn = evt.target.closest('button');
            const content = evt.target.closest('pre').querySelector('code').innerText;
            libdocUi.copyToClipboard(content, {notificationEnabled: false});
            if (elBtn.dataset.originalText === undefined) elBtn.dataset.originalText = elBtn.innerText;
            elBtn.innerHTML = `<span style="margin-left: -4px;"
                    class="d-flex | pos-absolute t-tX-100 | p-2 mr-1 | c-neutral-100 bc-success-500 brad-4">
                    <span class="icon-check pos-absolute top-50 left-50 t-tY-50 t-tX-50 | fs-1"></span>
                </span> ${libdocMessages.copied}!`;
            setTimeout(function() {
                elBtn.innerHTML = elBtn.dataset.originalText;
                elBtn.classList.remove('pe-none');
            }, 3000);
        },
        _scrollWindow: function() {
            libdocUi.updateGTTBtns();
        },
        _clickGTT: function(evt) {
            window.scroll({top:0});
            location.hash = '';
        },
        _clickFloatingToggleTocBtn: function(evt) {
            if (libdocUi.el.ftocDetails.open) {
                libdocUi.el.ftocDetails.open = false;
            } else {
                libdocUi.el.ftocDetails.open = true;
            }
        },
        _scrollWindowForFTOC: function() {
            libdocUi.updateFtocList();
        },
        _toggleFtocLargeDevices: function(evt) {
            if (libdocUi.el.ftocDetails.open) {
                libdocUi.updateUserPreferences({FTOCNormallyOpened: true});
                libdocUi.updateFtocList();
            } else {
                libdocUi.updateUserPreferences({FTOCNormallyOpened: false});
            }
        },
        _scrollNavPrimaryPreviousPreferenceValue: 0,
        _scrollNavPrimary: function() {
            const   previous = libdocUi.handlers._scrollNavPrimaryPreviousPreferenceValue,
                    current = libdocUi.el.navPrimary.scrollTop,
                    tolerance = 10,
                    lowBound = previous - tolerance,
                    highBound = previous + tolerance;
            if (current < lowBound || current > highBound) {
                libdocUi.updateUserPreferences({
                    navPrimaryScrollTop: libdocUi.el.navPrimary.scrollTop
                });
                libdocUi.handlers._scrollNavPrimaryPreviousPreferenceValue = current;
            }
        },
        _windowResize: function() {
            libdocUi._currentScreenSizeName = libdocUi.getCurrentScreenSizeName();
            libdocUi.updateSearchOccurrenceCmdBottom();
            libdocUi.updateNavPrimary();
            libdocUi.updateCustomLinks();
        },
        _windowLoad: function() {
            const textQuery = libdocUi._searchParams.get('text') || libdocUi._searchParams.get('search');
            if (textQuery !== null) {
                if (location.pathname == '/search/') {
                    document.title += ` “${textQuery}“`;
                    history.replaceState(null, '', `?search=${textQuery}`);
                } else if (location.pathname.indexOf("/tags/") !== 0) {
                    libdocUi.searchContent(textQuery);
                }
                libdocUi.el.searchInputs.forEach(function(elInput) {
                    elInput.value = textQuery;
                });
            }
            libdocUi.updateSearchInputClearBtns();
            libdocUi.updateTransferSizeDisplay();
        },
        _navPrimaryCheckboxChange: function(evt) {
            libdocUi.updateNavPrimary();
            libdocUi.updateFTOCBtns();
            libdocUi.updateGTTBtns();
        },
        _searchSubmit: function(evt) {
            const elInput = evt.target.querySelector('input');
            if (elInput !== null) {
                const elLabel = document.querySelector(`label[for="${elInput.id}"]`);
                if (elInput.value.length < 3) {
                    evt.preventDefault();
                    elLabel.innerText = libdocMessages.searchMinimumCharacters;
                    elLabel.style.color = 'var(--ita-colors-warning-500)';
                } else {
                    elLabel.innerText = libdocMessages.search;
                    elLabel.style.color = null;
                }
            }
        },
        _clickSearchInputClear: function(evt) {
            const elClearBtn = evt.target.closest('button');
            if (elClearBtn !== null) {
                elClearBtn.form.reset();
                elClearBtn.hidden = true;
                elClearBtn.form.querySelector('input[type="search"][name="search"]').focus();
            }
        },
        _clickAbbr: function(evt) {
            evt.target.classList.add('expanded');
            evt.target.dataset.title = evt.target.title;
            evt.target.removeEventListener('click', libdocUi.handlers._clickAbbr);
            evt.target.removeAttribute('title');
        },
        _DOMContentLoaded: function() {
            libdocUi.initKeyShortcuts();
        }
    },
    fitSvgToItsContent: function(svgElement) {
        // https://typeofnan.dev/how-to-perfectly-fit-an-svg-to-its-contents-using-javascript/
        const svg = svgElement;
        const { xMin, xMax, yMin, yMax } = [...svg.children].reduce((acc, el) => {
        const { x, y, width, height } = el.getBBox();
        if (!acc.xMin || x < acc.xMin) acc.xMin = x;
        if (!acc.xMax || x + width > acc.xMax) acc.xMax = x + width;
        if (!acc.yMin || y < acc.yMin) acc.yMin = y;
        if (!acc.yMax || y + height > acc.yMax) acc.yMax = y + height;
            return acc;
        }, {});

        const viewbox = `${xMin} ${yMin} ${xMax - xMin} ${yMax - yMin}`;

        svg.setAttribute('viewBox', viewbox);
    },
    updateTransferSizeDisplay: function() {
        const currentTransferSize = libdocUi.getTransferSize();
        if (currentTransferSize > 0) {
            document.querySelectorAll('.page-transfer-size-display').forEach(function(el) {
                el.innerHTML = `${currentTransferSize} kB`;
            })
        }
    },
    updateSearchInputClearBtns: function() {
        libdocUi.el.searchInputs.forEach(function(elInput) {
            const elClearBtn = elInput.form.querySelector('.search_form__clear_btn');
            if (elClearBtn !== null) {
                if (elInput.value.length > 0) {
                    elClearBtn.hidden = false;
                } else {
                    elClearBtn.hidden = true;
                }
            }
        });
    },
    toggleFtocSmallDevices: function() {
        if (libdocUi.el.ftocDetails.open) {
            libdocUi.el.ftocDetails.open = false;
            libdocUi.el.navSmallDevicesFTOCBtn.classList.add('c-primary-900');
            libdocUi.el.navSmallDevicesFTOCBtn.classList.remove('c-primary-500');
        } else {
            libdocUi.el.ftocDetails.open = true;
            libdocUi.el.ftoc.style.display = null;
            libdocUi.updateFtocList();
            libdocUi.el.navSmallDevicesFTOCBtn.classList.remove('c-primary-900');
            libdocUi.el.navSmallDevicesFTOCBtn.classList.add('c-primary-500');
        }
    },
    getVisibleTocIndexes: function() {
        const linkIndexesArray = [];
        if (typeof libdocUi.el.ftocLinks == 'object') {
            libdocUi.el.ftocLinks.forEach(function(elLink, linkIndex) {
                const   headingRects = libdocUi.el.ftocHeadings[linkIndex].getBoundingClientRect(),
                        nextIndex = linkIndex + 1,
                        elNextHeading = libdocUi.el.ftocHeadings[nextIndex];
                let nextHeadingRects = 0;
                if (elNextHeading !== undefined) nextHeadingRects = elNextHeading.getBoundingClientRect();
                if (headingRects.y >= -10 && headingRects.y < window.innerHeight - 50
                    || headingRects.y < -10 && nextHeadingRects.y >= window.innerHeight - 50
                    || headingRects.y < -10 && elNextHeading === undefined) {
                    linkIndexesArray.push(true);
                } else {
                    linkIndexesArray.push(false);
                }
            });
        }
        return linkIndexesArray;
    },
    createFloatingToc: function() {;
        if (libdocUi.el.ftoc === undefined && libdocUi.el.tocMainOl !== null) {
            libdocUi.el.ftocDetails = document.createElement('details');
            const elDetails = libdocUi.el.ftocDetails;
            elDetails.setAttribute('w-100', 'xs,sm');
            elDetails.id = 'floating_toc';
            const elSummary = document.createElement('summary');
            elSummary.setAttribute('class', 'd-flex jc-end | pt-5 | cur-pointer');
            elSummary.setAttribute('d-none', 'xs,sm');
            elSummary.title = libdocMessages.toggleFloatingToc;
            elSummary.ariaLabel = libdocMessages.tableOfContent;
            elSummary.innerHTML = `
                <span class="d-flex jc-center ai-center gap-2 | pos-relative ar-square | h-50px | brad-4 c-primary-500 bc-neutral-100 bwidth-1 bstyle-dashed bcolor-neutral-500 __hover-1 __soft-shadow">
                    <span class="icon-list-dashes fs-6"></span>
                </span>`;
            elDetails.appendChild(elSummary);
            
            let floatingTocMarkup = `
                <div id="floating_toc__list_parent"
                    d-flex="md"
                    jc-end="md">
                    <ul id="floating_toc__list"
                        class="
                        d-flex fd-column
                        pos-relative
                        o-auto pl-0 mb-0 pt-3 pb-3
                        lsp-3
                        bc-primary-100 blwidth-0 bwidth-1 bstyle-dashed bcolor-primary-300 ls-none
                        __soft-shadow"
                        fw-wrap="xs,sm"
                        mt-2="md"
                        mt-0="xs,sm"
                        maxh-200px="xs,sm"
                        brad-3="md"
                        bb-0="xs,sm"
                        br-0="xs,sm">`;
            libdocUi.el.ftocHeadings = [];
            libdocUi.el.tocMainOl.querySelectorAll('a').forEach(function(el) {
                const   headingReference = el.getAttribute(`href`),
                        elHeading = libdocUi.el.main.querySelector(headingReference);
                libdocUi.el.ftocHeadings.push(elHeading);
                floatingTocMarkup += `
                    <li>
                        <a  href="${headingReference}"
                            class="d-flex | pl-5 pr-5 | fs-3 lsp-3 lh-5 fvs-wght-400 td-none | c-primary-500 blwidth-1 blstyle-dashed bcolor-primary-300"
                            pt-2="md"
                            pb-2="md"
                            pt-1="xs,sm"
                            pb-1="xs,sm">
                            ${el.innerHTML}
                        </a>
                    </li>`;
            });
            floatingTocMarkup += '</ul></div>';
            elDetails.innerHTML += floatingTocMarkup;

            libdocUi.el.ftoc = document.createElement('div');
            libdocUi.el.ftoc.id = 'floating_toc_container';
            libdocUi.el.ftoc.setAttribute('class', 'd-flex | pos-fixed z-2');
            libdocUi.el.ftoc.setAttribute('top-0', 'md');
            libdocUi.el.ftoc.setAttribute('right-0', 'md');
            libdocUi.el.ftoc.setAttribute('left-0', 'xs,sm');
            libdocUi.el.ftoc.setAttribute('bottom-60px', 'xs,sm');
            libdocUi.el.ftoc.setAttribute('o-auto', 'xs,sm');
            libdocUi.el.ftoc.setAttribute('w-100', 'xs,sm');
            if (libdocUi._currentScreenSizeName == 'md') libdocUi.el.ftoc.style.display = 'none';
            libdocUi.el.ftoc.appendChild(elDetails);
            document.body.prepend(libdocUi.el.ftoc);
            window.addEventListener('scroll', libdocUi.handlers._scrollWindowForFTOC);
            libdocUi.el.ftocLinks = libdocUi.el.ftoc.querySelectorAll('a');
            libdocUi.el.ftocList = libdocUi.el.ftoc.querySelector('#floating_toc__list');
            libdocUi.el.navSmallDevicesFTOCBtn.disabled = false;
            libdocUi.el.navSmallDevicesFTOCBtn.addEventListener('click', libdocUi.toggleFtocSmallDevices);
            libdocUi.el.navSmallDevicesFTOCBtn.addEventListener('click', libdocUi.updateSearchOccurrenceCmdBottom);
            elDetails.addEventListener("toggle", libdocUi.handlers._toggleFtocLargeDevices);
            if (libdocUi.getUserPreferences().FTOCNormallyOpened) {
                elDetails.open = true;
                if (libdocUi._currentScreenSizeName == 'xs'
                    || libdocUi._currentScreenSizeName == 'sm') {
                    libdocUi.el.tocMain.open = false;
                }
            }
        }
    },
    createGoToTop: function() {
        if (libdocUi.el.gtt === undefined) {
            libdocUi.el.gtt = document.createElement('button');
            libdocUi.el.gtt.id = 'gtt_btn';
            libdocUi.el.gtt.setAttribute('class', 'd-none--xs d-none--sm | pos-fixed z-2 bottom-0 | p-0 h-50px ar-square mb-5 | fs-6 | brad-4 bc-neutral-100 bwidth-1 bstyle-dashed bcolor-neutral-500 cur-pointer __hover-1 __soft-shadow');
            libdocUi.el.gtt.innerHTML = `<span class="icon-arrow-line-up | pos-absolute top-50 left-50 t-tY-50 t-tX-50 | c-primary-500"></span>`;
            libdocUi.el.gtt.title = libdocMessages.goToTopOfPage;
            libdocUi.el.gtt.addEventListener('click', libdocUi.handlers._clickGTT);
            if (window.scrollY <= libdocUi.el.mainHeader.clientHeight) libdocUi.disableGTTLargeDevices();
            document.body.appendChild(libdocUi.el.gtt);
            window.addEventListener('scroll', libdocUi.handlers._scrollWindow);
        }
    },
    enableGTTLargeDevices: function() {
        libdocUi.el.gtt.classList.remove('d-none');
    },
    disableGTTLargeDevices: function() {
        libdocUi.el.gtt.classList.add('d-none');
    },
    enableGTTSmallDevices: function() {
        libdocUi.el.navSmallDevicesGTTBtn.disabled = false;
    },
    disableGTTSmallDevices: function() {
        libdocUi.el.navSmallDevicesGTTBtn.disabled = true;
    },
    updateGTTBtns: function() {
        if (window.scrollY > libdocUi.el.mainHeader.clientHeight) {
            libdocUi.enableGTTLargeDevices();
            if (getComputedStyle(libdocUi.el.navPrimaryContainer).display != 'none') {
                libdocUi.disableGTTSmallDevices();
            } else {
                libdocUi.enableGTTSmallDevices();
            }
        } else {
            libdocUi.disableGTTLargeDevices();
            libdocUi.disableGTTSmallDevices();
        }
    },
    updateNavPrimary: function() {
        const userPreferences = libdocUi.getLocalStorage(libdocUi.defaults.localStorageIdentifier);
        if (userPreferences?.navPrimaryScrollTop) {
            libdocUi.el.navPrimary.scroll({top: userPreferences?.navPrimaryScrollTop});
        } else {
            // Scroll to [aria-current="page"] element
            const   elCurrentPageLink = libdocUi.el.navPrimary.querySelector('[aria-current="page"]'),
                    elNavP = libdocUi.el.navPrimary;
            if (elCurrentPageLink !== null && elNavP !== null) {
                if (elCurrentPageLink.clientHeight + elCurrentPageLink.offsetTop > elNavP.clientHeight) {
                    elNavP.scroll({
                        top: (elCurrentPageLink.offsetTop - elCurrentPageLink.clientHeight)
                    });
                }
            }
        }
    },
    getUserPreferences: function() {
        return libdocUi.getLocalStorage(libdocUi.defaults.localStorageIdentifier) || {};
    },
    updateUserPreferences: function(newPreferences) {
        if (typeof newPreferences == 'object' && newPreferences !== null) {
            const currentUserPreference = libdocUi.getLocalStorage(libdocUi.defaults.localStorageIdentifier);
            if (currentUserPreference === null) {
                libdocUi.saveLocalStorage({
                    identifier: libdocUi.defaults.localStorageIdentifier,
                    backup: newPreferences
                });
            } else {
                let newStorage = {};
                for (const key in currentUserPreference) {
                    newStorage[key] = currentUserPreference[key];
                }
                for (const key in newPreferences) {
                    newStorage[key] = newPreferences[key];
                }
                libdocUi.saveLocalStorage({
                    identifier: libdocUi.defaults.localStorageIdentifier,
                    backup: newStorage
                });
            }
        }
    },
    updateFTOCBtns: function() {
        if (libdocUi.el.tocMainOl !== null) {
            if (getComputedStyle(libdocUi.el.navPrimaryContainer).display != 'none') {
                libdocUi.el.navSmallDevicesFTOCBtn.disabled = true;
            } else {
                libdocUi.el.navSmallDevicesFTOCBtn.disabled = false;
            }
            if (libdocUi.el.ftocDetails.open) {
                libdocUi.el.navSmallDevicesFTOCBtn.classList.remove('c-primary-900');
                libdocUi.el.navSmallDevicesFTOCBtn.classList.add('c-primary-500');
            } else {
                libdocUi.el.navSmallDevicesFTOCBtn.classList.add('c-primary-900');
                libdocUi.el.navSmallDevicesFTOCBtn.classList.remove('c-primary-500');
            }
        }
    },
    updateFtocList: function() {
        if (window.scrollY > libdocUi.el.mainHeader.clientHeight && typeof libdocUi.el.ftoc == 'object') {
            libdocUi.el.ftoc.style.display = null;
            if (libdocUi.el.ftocDetails.open) {
                const linkIndexesArray = libdocUi.getVisibleTocIndexes();
                let firstTrueIndex = -1;
                linkIndexesArray.forEach(function(isInViewport, linkIndex) {
                    if (isInViewport) {
                        // libdocUi.el.ftocLinks[linkIndex].style.backgroundColor = 'var(--ita-colors-primary-200)';
                        libdocUi.el.ftocLinks[linkIndex].classList.add('__active');
                        if (firstTrueIndex === -1) firstTrueIndex = linkIndex;
                    } else {
                        // libdocUi.el.ftocLinks[linkIndex].style.backgroundColor = null;
                        libdocUi.el.ftocLinks[linkIndex].classList.remove('__active');
                    }
                });
                if (firstTrueIndex > -1) {
                    const elFirstLink = libdocUi.el.ftocLinks[firstTrueIndex];
                    if (libdocUi._currentScreenSizeName == 'md') {
                        if (
                            (elFirstLink.offsetTop + elFirstLink.clientHeight > libdocUi.el.ftocList.scrollTop)
                            &&
                            (elFirstLink.offsetTop + elFirstLink.clientHeight < libdocUi.el.ftocList.scrollTop + libdocUi.el.ftocList.clientHeight)
                            ) {
                        } else {
                            libdocUi.el.ftocList.scroll({top: libdocUi.el.ftocLinks[firstTrueIndex].offsetTop - 80});
                        }
                    } else {
                        if (
                            (elFirstLink.offsetLeft + elFirstLink.clientWidth / 2 > libdocUi.el.ftocList.scrollLeft)
                            &&
                            (elFirstLink.offsetLeft + elFirstLink.clientWidth < libdocUi.el.ftocList.scrollLeft + libdocUi.el.ftocList.clientWidth)
                            ) {
                        } else {
                            libdocUi.el.ftocList.scroll({left: libdocUi.el.ftocLinks[firstTrueIndex].offsetLeft - 10});
                        }
                    }
                }
            }
        } else {
            if (typeof libdocUi.el.ftoc == 'object') {
                if (libdocUi._currentScreenSizeName == 'md') libdocUi.el.ftoc.style.display = 'none';
            }
        }
    },
    updateSearchOccurrenceCmdBottom: function() {
        if (libdocUi.el.searchOccurrencesCmd !== undefined) {
            libdocUi._so.bottomSpacing = 0;
            if (libdocUi._currentScreenSizeName == 'xs' || libdocUi._currentScreenSizeName == 'sm') {
                const fTocHeight = libdocUi.el.ftoc?.clientHeight || 0;
                libdocUi._so.bottomSpacing = libdocUi.el.navSmallDevices.clientHeight + fTocHeight;
            }
            libdocUi.el.searchOccurrencesCmd.style.bottom = `${libdocUi._so.bottomSpacing}px`;
        }
    },
    createSearchOccurencesCmd: function() {
        if (typeof libdocUi.el.main == 'object'
            && typeof libdocUi.el.searchOccurrencesCmd === 'undefined') {
            libdocUi.el.searchOccurrencesCmd = document.createElement('nav');
            libdocUi.el.searchOccurrencesCmd.id = 'query_occurrences_cmd';
            libdocUi.el.searchOccurrencesCmd.setAttribute('class', 'd-flex fw-wrap jc-space-between ai-center gap-5 | pos-sticky bottom-0 z-1 | pb-5 pt-5 | bs-1 bc-success-100 bradtl-3 bradtr-3');
            const text = new URLSearchParams(location.search).get('text') || '';
            libdocUi.el.searchOccurrencesCmd.innerHTML = `
                <p class="d-flex ai-baseline gap-2 | m-0 | fs-2">
                    ${libdocMessages.searchOccurrence}
                    <strong class="pt-1 pb-1 pl-3 pr-3 | fvs-500 | bc-success-900 c-success-100 brad-1">${text}</strong>
                </p>
                <div class="d-flex gap-2">
                    <button type="button"
                        class="pos-relative | h-50px ar-square | fs-5 | brad-4 bc-neutral-100 c-success-900 bwidth-1 bstyle-dashed bcolor-success-900 cur-pointer __hover-2"
                        onclick="libdocUi.prevSearchOccurrence()"
                        title="${libdocMessages.searchOccurrencesPrevious}">
                        <span class="icon-caret-left | pos-absolute top-50 left-50 t-tY-50 t-tX-50 | c-success-900"></span>
                    </button>
                    <button type="button"
                        class="pos-relative | h-50px ar-square | fs-2 | brad-4 bc-neutral-100 c-success-900 bwidth-1 bstyle-dashed bcolor-success-900 cur-pointer __hover-2"
                        onclick="libdocUi.curSearchOccurrence()"
                        title="${libdocMessages.searchOccurrencesCurrent}">
                        <span id="current_query_occurrence_index_position" class="pos-absolute top-50 left-50 t-tY-50 t-tX-50 | c-success-900"></span>
                    </button>
                    <button type="button"
                        class="pos-relative | h-50px ar-square | fs-5 | brad-4 bc-neutral-100 c-success-900 bwidth-1 bstyle-dashed bcolor-success-900 cur-pointer __hover-2"
                        onclick="libdocUi.nextSearchOccurrence()"
                        title="${libdocMessages.searchOccurrencesNext}">
                        <span class="icon-caret-right | pos-absolute top-50 left-50 t-tY-50 t-tX-50 | c-success-900"></span>
                    </button>
                    <button type="button"
                        class="pos-relative | h-50px ar-square | fs-2 | brad-4 bc-neutral-100 c-success-900 bwidth-1 bstyle-dashed bcolor-success-900 cur-pointer __hover-2"
                        onclick="libdocUi.stopSearchOccurrence()"
                        title="${libdocMessages.searchOccurrencesStop}">
                        <span class="icon-x | pos-absolute top-50 left-50 t-tY-50 t-tX-50 | c-success-900"></span>
                    </button>
                </div>`;
            libdocUi.el.main.append(libdocUi.el.searchOccurrencesCmd);
            libdocUi.el.searchOccurrencesCurrentIndexPosition = document.querySelector('#current_query_occurrence_index_position');
        }
    },
    _currentScreenSizeName: '',
    _searchParams: new URLSearchParams(location.search),
    goToOccurrence: function(index) {
        if (typeof index == 'number') {
            if (index > -1 && index < libdocUi._so.els.length) {
                libdocUi._so.els.forEach(function(el) {
                    el.classList.remove('__search-occurrence');
                });
                // const scrollTop = libdocUi._so.els[index].getBoundingClientRect().top - libdocUi.el.searchOccurrencesCmd.clientHeight - 20;
                // window.scroll({top: scrollTop});
                libdocUi._so.els[index].scrollIntoView();
                window.scroll({top: window.scrollY - 100});
                libdocUi._so.curIndex = index;
                libdocUi.el.searchOccurrencesCurrentIndexPosition.innerText = `${libdocUi._so.curIndex + 1}/${libdocUi._so.els.length}`;
                libdocUi._so.els[index].classList.add('__search-occurrence');
                
            }
        }
    },
    prevSearchOccurrence: function() {
        if (libdocUi._so.curIndex > 0) {
            const newIndex = libdocUi._so.curIndex - 1;
            libdocUi.goToOccurrence(newIndex);
        } else if (libdocUi._so.curIndex === 0) {
            libdocUi.goToOccurrence(libdocUi._so.els.length - 1);
        }
    },
    nextSearchOccurrence: function() {
        if (libdocUi._so.curIndex < libdocUi._so.els.length - 1) {
            const newIndex = libdocUi._so.curIndex + 1;
            libdocUi.goToOccurrence(newIndex);
        } else if (libdocUi._so.curIndex === libdocUi._so.els.length - 1) {
            libdocUi.goToOccurrence(0);
        }
    },
    curSearchOccurrence: function() {
        libdocUi.goToOccurrence(libdocUi._so.curIndex);
    },
    stopSearchOccurrence: function() {
        libdocUi._so.els.forEach(function(el) {
            el.classList.remove('__search-occurrence');
            libdocUi.el.searchOccurrencesCmd.classList.remove('d-flex');
            libdocUi.el.searchOccurrencesCmd.classList.add('d-none');
        });
        libdocUi.el.searchInputs.forEach(function(elInput) {
            elInput.value = '';
        });
        libdocUi.updateSearchInputClearBtns();
        history.pushState(null, '', location.pathname);
    },
    // Search occurrences
    _so: {
        // elements containing query occurrence
        els: [],
        // Current occurrence index
        curIndex: 0,
        bottomSpacing: 0
    },
    getTextContentWithoutChildNodes: function(el) {
        // Source https://medium.com/@roxeteer/javascript-one-liner-to-get-elements-text-content-without-its-child-nodes-8e59269d1e71
        if (typeof el == 'object') return [].reduce.call(el.childNodes, function(a, b) { return a + (b.nodeType === 3 ? b.textContent : ''); }, '');
    },
    searchContent: function(query) {
        if (typeof query == 'string') {
            libdocUi._so.els = [];
            const queryLC = query.toLowerCase();
            // Every child of main excepting pre, aside and header
            document.querySelectorAll('main>*:not(pre):not(aside):not(header), main>*:not(pre):not(aside):not(header) *, .page_tag').forEach(function(el) {
                const textContentWoChildren = libdocUi.getTextContentWithoutChildNodes(el);
                if (textContentWoChildren.toLowerCase().includes(queryLC)) {
                    libdocUi._so.els.push(el);
                }
            });
            // For sandboxes and pre
            document.querySelectorAll('main>pre, main>.sandbox').forEach(function(el) {
                if (el.innerText.toLowerCase().includes(queryLC)) {
                    libdocUi._so.els.push(el);
                }
            });
            if (libdocUi._so.els.length > 0) {
                libdocUi.createSearchOccurencesCmd();
                libdocUi.updateSearchOccurrenceCmdBottom();
                libdocUi.goToOccurrence(0);
                document.title += ` | “${query}“`;
                history.replaceState(null, '', `?text=${query}`);
            }
        }
    },
    setColorScheme: function(name) {
        if (typeof name == 'string') {
            if (libdocUi.defaults.colorSchemes.includes(name)) {
                if (name == 'light') {
                    libdocUi.el.darkModeCssMetaLink.href = '';
                    libdocUi.el.darkModeCssMetaLink.media = libdocUi.defaults.darkModeCssMedia;
                } else if (name == 'dark') {
                    libdocUi.el.darkModeCssMetaLink.href = libdocUi.defaults.darkModeCssFilePath;
                    libdocUi.el.darkModeCssMetaLink.media = '';
                } else if (name == 'auto') {
                    libdocUi.el.darkModeCssMetaLink.href = libdocUi.defaults.darkModeCssFilePath;
                    libdocUi.el.darkModeCssMetaLink.media = libdocUi.defaults.darkModeCssMedia;
                }
                libdocUi.el.inputsColorScheme.forEach(function(elInput) {
                    if (elInput.value == name) elInput.checked = true;
                })
                libdocUi.updateUserPreferences({
                    colorScheme: name
                });
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
    createCopyCodeOnCodeBlocks: function() {
        const elsPre = document.querySelectorAll('main>pre');
        if (elsPre.length > 0) {
            elsPre.forEach(function(elPre) {
                elPre.style.paddingTop = '0';
                const elCommands = elPre.querySelector('.copy_code_block');
                if (elCommands === null) {
                    const commandBarMarkup = `<div class="d-flex jc-end | pos-relative">
                            <button type="button"
                                class="
                                d-flex ai-center
                                pt-5 pb-5 fvs-wght-400 fs-2 tt-uppercase
                                bc-0 c-primary-900 b-0 cur-pointer
                                copy_code_block">${libdocMessages.copyCode}</button>
                        </div>`;
                    elPre.insertAdjacentHTML('afterbegin', commandBarMarkup);
                }
                const elCode = elPre.querySelector('code');
                if (elCode !== null) {
                    const className = elCode.getAttribute('class');
                    if (className !== null) {
                        const languageClassSplit = elCode.getAttribute('class').split(' ');
                        if (languageClassSplit.length > 0) elCode.dataset.languageName = languageClassSplit[0].toString().replace('language-', '');
                    }
                }
            });
            // Adjust proper language name display
            const languagesNamesArray = libdocUi.getJson(libdocUi.defaults.supportedLanguagesJsonPath);
            languagesNamesArray.then(languagesArray => {
                if (languagesArray.length > 0) {
                    document.querySelectorAll('code[data-language-name]').forEach(function(elCode) {
                        const languageAlias = elCode.dataset.languageName;
                        let index = -1;
                        languagesArray.forEach(function(lang, langIndex) {
                            if (lang.includes(languageAlias)) index = langIndex;
                        });
                        if (index > -1) {
                            const languageName = languagesArray[index].split('|')[1];
                            elCode.dataset.languageName = languageName;
                        }
                    })
                }
            });
        }
    },
    initKeyShortcuts: function() {
        if (typeof hotkeys == 'function') {
            hotkeys('s', function (event, handler) {
                // Set timeout to avoid shortcut letter to be typed into input field
                if (handler.key == 's') setTimeout(function() { fuzzy.el.searchInput.focus()},100);
            });
        }
    },
    addExternalLinkIconIntoMainContent: function() {
        libdocUi.el.main.querySelectorAll('main a[href^="https://"]').forEach(function(el) {
            const link = new URL(el.href);
            if (link.hostname != location.hostname) {
                el.target = '_blank';
                el.title = `${libdocMessages.open} ${el.href} ${libdocMessages.inANewTab.toLowerCase()}`;
                if (link.hostname == libdocSystem.productionUrl) {
                    el.classList.add('__external-link');
                }
            }
        });
    },
    _updateCustomLinks: null,
    updateCustomLinks: function() {
        if (libdocUi.el.customLinks !== null && libdocUi.el.navPrimaryContainer !== null) {
            const   ctnWidth = libdocUi.el.navPrimaryContainer.clientWidth,
                    elsLinks = libdocUi.el.customLinks.querySelectorAll('a'),
                    isLargeScreen = libdocUi.getCurrentScreenSizeName() == 'md' ? true : false;
            if (elsLinks.length > 1 && isLargeScreen && libdocUi._updateCustomLinks === null) {
                libdocUi._updateCustomLinks = {
                    itemsWidth: 0,
                    items: []
                };
                elsLinks.forEach(function(elLink) {
                    libdocUi._updateCustomLinks.items.push({
                        url: elLink.href,
                        text: elLink.innerHTML.trim(),
                        classNames: elLink.getAttribute('class'),
                        width: elLink.clientWidth
                    });
                    libdocUi._updateCustomLinks.itemsWidth += elLink.clientWidth;
                });
                libdocUi.el.customLinks.innerHTML = '';
                let     tempWidth = 0;
                const   menuItems = [],
                        paddingLeft = parseFloat(getComputedStyle(libdocUi.el.customLinks).paddingLeft),
                        threshold = ctnWidth - 35 - paddingLeft;
                libdocUi._updateCustomLinks.items.forEach(function(item) {
                    tempWidth += item.width;
                    const elLink = document.createElement('a');
                    elLink.href = item.url;
                    elLink.innerHTML = item.text;
                    elLink.title = `${libdocMessages.open} ${item.text} ${libdocMessages.inANewTab}`;
                    elLink.target = '_blank';
                    if (tempWidth > threshold) {
                        elLink.setAttribute('class', 'd-flex ai-center gap-1 | pt-3 pb-3 p-5 | fvs-wght-700 fs-2 lsp-3 lh-1 tt-uppercase td-none ws-nowrap | c-primary-600');
                        menuItems.push(elLink);
                    } else {
                        elLink.setAttribute('class', item.classNames);
                        libdocUi.el.customLinks.appendChild(elLink);
                    }
                });
                if (menuItems.length > 0) {
                    const   elDetails = document.createElement('details'),
                            elSummary = document.createElement('summary'),
                            elMenuItemsCtn = document.createElement('nav');
                    elMenuItemsCtn.setAttribute('class', 'd-flex fd-column | pos-absolute right-0 | mr-3 | bc-neutral-100 bwidth-1 bstyle-dashed bcolor-neutral-500 brad-2 __soft-shadow');
                    elDetails.setAttribute('class', 'pos-absolute right-0');
                    elSummary.setAttribute('class', 'd-flex ai-center jc-end gap-1 | pt-2 pb-2 pl-4 pr-4 | lh-1 | cur-pointer c-primary-600');
                    elSummary.setAttribute('title', libdocMessages.otherCustomLinks);
                    elSummary.innerHTML = '<span class="icons"><span class="icon-plus-circle"></span><span class="icon-minus-circle"></span></span>';
                    elDetails.appendChild(elSummary);
                    menuItems.forEach(function(elItem) {
                        elMenuItemsCtn.appendChild(elItem);
                    });
                    elDetails.appendChild(elMenuItemsCtn);
                    libdocUi.el.customLinks.appendChild(elDetails);
                    libdocUi.el.customLinks.classList.remove('o-auto');
                } else {
                    libdocUi.el.customLinks.classList.add('o-auto');
                }
            }
        }
    },
    update: function() {
        libdocUi.defaults.darkModeCssMedia = libdocUi.el.darkModeCssMetaLink.media;
        libdocUi.setColorScheme(libdocUi.getUserPreferences().colorScheme);
        libdocUi._currentScreenSizeName = libdocUi.getCurrentScreenSizeName();
        hljs.highlightAll();
        libdocUi.createCopyCodeOnCodeBlocks();
        libdocUi.createFloatingToc();
        libdocUi.createGoToTop();
        libdocUi.updateNavPrimary();
        libdocUi.updateFtocList();
        libdocUi.updateGTTBtns();
        libdocUi.addExternalLinkIconIntoMainContent();
        libdocUi.updateCustomLinks();
        libdocUi.el.navPrimaryCheckbox.addEventListener('change', libdocUi.handlers._navPrimaryCheckboxChange);
        window.addEventListener('resize', libdocUi.handlers._windowResize);
        window.addEventListener('load', libdocUi.handlers._windowLoad);
        libdocUi.el.navPrimary.addEventListener('scroll', libdocUi.handlers._scrollNavPrimary);
        document.querySelectorAll('.copy_code_block').forEach(function(el) {
            el.addEventListener('click', libdocUi.handlers._clickCopyCodeBlock);
        });
        libdocUi.el.searchForms.forEach(function(elForm) {
            elForm.addEventListener('submit', libdocUi.handlers._searchSubmit);
        });
        libdocUi.el.searchInputs.forEach(function(elInput) {
            elInput.addEventListener('input', libdocUi.updateSearchInputClearBtns);
        });
        libdocUi.el.searchClearBtns.forEach(function(elClearBtn) {
            elClearBtn.addEventListener('click', libdocUi.handlers._clickSearchInputClear);
        });
        document.querySelectorAll('details[name="nav_primary"]').forEach(function(elDetail) {
            elDetail.addEventListener("toggle", libdocUi.handlers._toggleNavPrimaryAccordion);
        });
        libdocUi.el.main.querySelectorAll('abbr[title]').forEach(function(el) {
            el.addEventListener('click', libdocUi.handlers._clickAbbr);
        });
        document.body.addEventListener('touchstart', libdocUi.handlers._touchStart);
        libdocUi.el.inputsColorScheme.forEach(function(elInput) {
            elInput.addEventListener('click', libdocUi.handlers._colorSchemeClick);
        });
        document.addEventListener('DOMContentLoaded', libdocUi.handlers._DOMContentLoaded);
    }
}
libdocUi.update();