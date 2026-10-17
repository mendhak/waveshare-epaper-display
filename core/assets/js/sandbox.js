const sandbox = {
    _pointerX: 0,
    _pointerY: 0,
    _pointerXReference: 0,
    _pointerYReference: 0,
    _preInitialWidth: null,
    _iframeInitialWidth: null,
    _resizerEls: {
        btn: null,
        sandboxWrapper: null,
        pre: null,
        iframe: null,
        tabCode: null,
        tabIframe: null,
        monitorIframeWidth: null,
        monitorIframeHeight: null
    },
    _selectors: {
        sandbox: '.sandbox',
        resizer: '.sandbox__resizer',
        codeWrapper: '.sandbox__code_wrapper',
        iframeWrapper: '.sandbox__iframe_wrapper',
        code: '.sandbox__code',
        iframe: '.sandbox__iframe',
        tabBtn: '.sandbox__tab',
        monitorIframeWidth: '.sandbox__monitor__iframe_width',
        monitorIframeHeight: '.sandbox__monitor__iframe_height',
        copyCode: '.sandbox__copy_code',
        reload: '.sandbox__reload',
        copyUrl: '.sandbox__copy_url',
        permalink: '.sandbox__permalink'
    },
    disableIframes: function() {
        document.querySelectorAll(sandbox._selectors.iframe).forEach(function(el) {
            el.classList.add('pe-none');
        });
    },
    enableIframes: function() {
        document.querySelectorAll(sandbox._selectors.iframe).forEach(function(el) {
            el.classList.remove('pe-none');
        });
    },
    resize: function() {
        const   delta = sandbox._pointerX - sandbox._pointerXReference,
                preWidth = sandbox._preInitialWidth + delta,
                iframeWidth = sandbox._iframeInitialWidth - delta;
        if (preWidth > 0 && iframeWidth > 0) {
            sandbox._resizerEls.pre.style.width = `${preWidth}px`;
            sandbox._resizerEls.iframe.style.width = `${iframeWidth}px`;
            sandbox._resizerEls.monitorIframeWidth.innerHTML = iframeWidth;
            sandbox._resizerEls.monitorIframeHeight.innerHTML = sandbox._resizerEls.iframe.querySelector('iframe').clientHeight;
        }
    },
    reset: function() {
        document.querySelectorAll(`${sandbox._selectors.codeWrapper}, ${sandbox._selectors.iframeWrapper}`).forEach(function(el) {
            el.style.width = null;
        });
        sandbox.updateMonitor();
    },
    updateMonitor: function() {
        document.querySelectorAll(sandbox._selectors.sandbox).forEach(function(elSandbox) {
            elSandbox.querySelectorAll(`${sandbox._selectors.codeWrapper}, ${sandbox._selectors.iframeWrapper}`).forEach(function(el) {
                el.style.width = null;
            });
            const elIframe = elSandbox.querySelector('iframe');
            elSandbox.querySelector(sandbox._selectors.monitorIframeWidth).innerHTML = elIframe.offsetWidth;
            elSandbox.querySelector(sandbox._selectors.monitorIframeHeight).innerHTML = elIframe.offsetHeight;
        });
    },
    handlers: {
        _mousedownResizer: function(evt) {
            sandbox._pointerXReference = evt.clientX;
            sandbox._resizerEls.btn = evt.target.closest(sandbox._selectors.resizer);
            sandbox._resizerEls.sandboxWrapper = evt.target.closest(sandbox._selectors.sandbox);
            sandbox._resizerEls.pre = sandbox._resizerEls.sandboxWrapper.querySelector(sandbox._selectors.codeWrapper);
            sandbox._resizerEls.iframe = sandbox._resizerEls.sandboxWrapper.querySelector(sandbox._selectors.iframeWrapper);
            sandbox._resizerEls.monitorIframeWidth = sandbox._resizerEls.sandboxWrapper.querySelector(sandbox._selectors.monitorIframeWidth);
            sandbox._resizerEls.monitorIframeHeight = sandbox._resizerEls.sandboxWrapper.querySelector(sandbox._selectors.monitorIframeHeight);
            if (typeof sandbox._resizerEls.btn == 'object'
                && typeof sandbox._resizerEls.sandboxWrapper == 'object'
                && typeof sandbox._resizerEls.pre == 'object'
                && typeof sandbox._resizerEls.iframe == 'object'
                && typeof sandbox._resizerEls.monitorIframeWidth == 'object'
                && typeof sandbox._resizerEls.monitorIframeHeight == 'object') {
                sandbox._iframeInitialWidth = sandbox._resizerEls.iframe.clientWidth;
                sandbox._preInitialWidth = sandbox._resizerEls.pre.clientWidth;
                // To be able to detect mouse position
                sandbox.disableIframes();
                // Enable mouse position monitoring
                window.addEventListener('mousemove', sandbox.handlers._mousemoveWindow);
            }
        },
        _stopResizer: function(evt) {
            sandbox.enableIframes();
            window.removeEventListener('mousemove', sandbox.handlers._mousemoveWindow);
        },
        _mousemoveWindow:  function(evt) {
            sandbox._pointerX = evt.clientX;
            sandbox._pointerY = evt.clientY;
            sandbox.resize();
        },
        _tab: function(evt) {
            const elBtn = evt.target.closest(sandbox._selectors.tabBtn),
                elSandbox = evt.target.closest(sandbox._selectors.sandbox),
                elsBtns = elSandbox.querySelectorAll(sandbox._selectors.tabBtn),
                elPre = elSandbox.querySelector(sandbox._selectors.codeWrapper),
                elIframe = elSandbox.querySelector(sandbox._selectors.iframeWrapper),
                tabName = elBtn.dataset.name;
            switch (tabName) {
                case 'code':
                    elPre.classList.remove('d-none--xs', 'd-none--sm');
                    elIframe.classList.add('d-none--xs', 'd-none--sm');
                    break;
            
                default:
                    elIframe.classList.remove('d-none--xs', 'd-none--sm');
                    elPre.classList.add('d-none--xs', 'd-none--sm');
                    break;
            }
            elsBtns.forEach(function(el) {
                el.classList.remove('__active');
            });
            elBtn.classList.add('__active');
        },
        _clickCopyCode: function(evt) {
            const elBtn = evt.target.closest('button');
            const code = evt.target.closest(sandbox._selectors.sandbox).querySelector(sandbox._selectors.code).innerText;
            elBtn.classList.add('pe-none');
            libdocUi.copyToClipboard(code, {notificationEnabled: false});
            if (elBtn.dataset.originalText === undefined) elBtn.dataset.originalText = elBtn.innerText;
            elBtn.innerHTML = `
                <span style="margin-left: -4px;"
                    class="d-flex | pos-absolute t-tX-100 | p-2 mr-1 | brad-4 bc-success-500">
                    <span class="icon-check pos-absolute top-50 left-50 t-tY-50 t-tX-50 | fs-1 | c-success-100"></span>
                </span>
                ${libdocMessages.copied}!`;
            setTimeout(function() {
                elBtn.innerHTML = elBtn.dataset.originalText;
                elBtn.classList.remove('pe-none');
            }, 3000);
        },
        _clickCopyUrl: function(evt) {
            const elBtn = evt.target.closest('button');
            const permalink = evt.target.closest(sandbox._selectors.sandbox).querySelector(sandbox._selectors.permalink).href;
            elBtn.classList.add('pe-none');
            libdocUi.copyToClipboard(permalink, {notificationEnabled: false});
            if (elBtn.dataset.originalText === undefined) elBtn.dataset.originalText = elBtn.innerText;
            elBtn.innerHTML = `
                <span style="margin-left: -4px;"
                    class="d-flex | pos-absolute t-tX-100 | p-2 mr-1 | brad-4 bc-success-500">
                    <span class="icon-check pos-absolute top-50 left-50 t-tY-50 t-tX-50 | fs-1 | c-success-100"></span>
                </span>
                ${libdocMessages.copied}!`;
            setTimeout(function() {
                elBtn.innerHTML = elBtn.dataset.originalText;
                elBtn.classList.remove('pe-none');
            }, 3000);
        },
        _clickReload: function(evt) {
            const elBtn = evt.target.closest('button');
            const elIframe = evt.target.closest(sandbox._selectors.sandbox).querySelector(sandbox._selectors.iframe);
            const elTargetDocument = elIframe.contentWindow.document;
            const elTargetWindow = elIframe.contentWindow.window;
            elBtn.classList.add('pe-none');
            elTargetDocument.location.reload();
            elTargetWindow.scroll(0,0);
            if (elBtn.dataset.originalText === undefined) elBtn.dataset.originalText = elBtn.innerText;
            elBtn.innerHTML = `
                <span style="margin-left: -4px;"
                    class="d-flex | pos-absolute t-tX-100 | p-2 mr-1 | brad-4 bc-success-500">
                    <span class="icon-check pos-absolute top-50 left-50 t-tY-50 t-tX-50 | fs-1 | c-success-100"></span>
                </span>
                ${libdocMessages.reloaded}!`;
            setTimeout(function() {
                elBtn.innerHTML = elBtn.dataset.originalText;
                elBtn.classList.remove('pe-none');
            }, 3000);
        }
    },
    update: function() {
        if (document.querySelector(sandbox._selectors.sandbox) !== null) {
            document.querySelectorAll(sandbox._selectors.resizer).forEach(function(el) {
                el.addEventListener('mousedown', sandbox.handlers._mousedownResizer);
            });
            document.querySelectorAll(sandbox._selectors.tabBtn).forEach(function(el) {
                el.addEventListener('click', sandbox.handlers._tab);
            });
            document.querySelectorAll(sandbox._selectors.copyCode).forEach(function(el) {
                el.addEventListener('click', sandbox.handlers._clickCopyCode);
            });
            document.querySelectorAll(sandbox._selectors.copyUrl).forEach(function(el) {
                el.addEventListener('click', sandbox.handlers._clickCopyUrl);
            });
            document.querySelectorAll(sandbox._selectors.reload).forEach(function(el) {
                el.addEventListener('click', sandbox.handlers._clickReload);
            });
            window.addEventListener('mouseup', sandbox.handlers._stopResizer);
            window.addEventListener('resize', sandbox.reset);
            sandbox.updateMonitor();
        }
    }
}
document.addEventListener('DOMContentLoaded', sandbox.update);