// START IMPORT REQUIRE WORKAROUND
// To make 11ty --serve work with JSON imports
// https://github.com/11ty/eleventy/issues/3128#issuecomment-1878745864
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const childProcess = require('child_process');
// END IMPORT REQUIRE WORKAROUND

// START JSON IMPORT WORKAROUND
// import libdocMessages   from "./libdocMessages.json" with { "type": "json" };
// import libdocSystem     from "./libdocSystem.json" with { "type": "json" };
const libdocSystem =        require("./libdocSystem.json");
const libdocMessages =      require("./libdocMessages.json");
// END JSON IMPORT WORKAROUND

import libdocUtils          from    "./libdocUtils.js";
import libdocConfig         from    "./libdocConfig.js";

export default {
    pluginsParameters: {
        eleventyImageTransform: function() {
            // https://www.11ty.dev/docs/plugins/image/#more-configuration-options
            const   params = libdocSystem.pluginsParameters.eleventyImageTransform,
                    w = libdocSystem.widthContent;
            return {
                // output image formats
                formats: params.formats,
                useCache: params.useCache,
                svgShortCircuit: params.svgShortCircuit,
                // output image widths
                widths: [
                    w + 30,
                    w * 2,
                    w * 4
                ],
                filenameFormat: function (id, src, width, format, options) {
                    // Define custom filenames for generated images
                    // id: hash of the original image
                    // src: original image path
                    // width: current width in px
                    // format: current file format
                    // options: set of options passed to the Image call
                    const filename = src.split('/').slice(-1)[0].split('.')[0];
                    return `${libdocUtils.slugify(filename)}-${id}-__${width}__.${format}`;
                },
                sharpOptions: {
                    animated: true
                },
                // transform: (sharp) => {
                //     sharp.trim();
                // },
                // optional, attributes assigned on <img> nodes override these values
                htmlOptions: params.htmlOptions
            }
        }
    },
    filters: {
        sanitizeJson: async function(value) {
            // Remove back slashes
            value = value.replaceAll('\\', '');
            // Remove extra spaces
            value = value.replace(/\s+/g, ' ').trim();
            return value;
        },
        autoids: async function(content) {
            let i = 0;
            const anchorsIds = [];
            content = content.replace(/<([a-zA-Z][a-zA-Z0-9_-]*)\b[^>]*>(.*?)<\/\1>/g, function(m,m1,m2){
                let newM = m;
                if (libdocConfig.tocHtmlTags.includes(m1)) {
                    // Add id to the specified html tags
                    let slugifiedId = libdocUtils.slugify(m2);
                    if (anchorsIds.includes(slugifiedId)) {
                        slugifiedId += `-${i}`;
                    }
                    anchorsIds.push(slugifiedId);
                    const invalidFirstCharacters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
                    if (invalidFirstCharacters.includes(slugifiedId[0])) slugifiedId = 'a_' + slugifiedId;
                    const markup = `
                        <${m1} id="${slugifiedId}" pl-9="xs,sm">
                            <a  href="#${slugifiedId}"
                                title="${m2}"
                                class="pos-absolute top-50 left-0 t-tY-50 | p-4 ml-1 | td-none | brad-4 bc-neutral-100 bwidth-1 bstyle-dashed bcolor-neutral-500 __hover-1 __soft-shadow"
                                ml-3="xs,sm">
                                <span class="icon-link-simple | pos-absolute top-50 left-50 t-tY-50 t-tX-50 | fs-4"></span>
                            </a>
                    `;
                    newM = m.replace(`<${m1}>`, markup);
                    i++;
                }
                return newM;
            });
            return content;
        },
        embed: async function(src) {
            try {
                const url = new URL(src);
                const content = `
                    <aside class="widget widget-embed">
                        <iframe src="${url}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            loading="lazy"
                            allowfullscreen></iframe>
                    </aside>`;
                return content;
            } catch (e) {
                console.log(`${src} is not a valid URL`);
                return '';
            }
        },
        cleanup: async function(content) {
            content = content.replaceAll(`<table`, `<div class="o-auto w-100 table-wrapper"><table`);
            content = content.replaceAll(`</table>`, `</table></div>`);
            content = content.replaceAll(`<p><div`, `<div`);
            content = content.replaceAll(`</div></p>`, `</div>`);
            content = content.replaceAll(`<p><aside`, `<aside`);
            content = content.replaceAll(`</aside></p>`, `</aside>`);
            return content;
        },
        datePrefixText: async function(date) {
            let text = '';
            if (typeof date == 'string') {
                text = libdocMessages.lastModified[libdocConfig.lang];
            }
            return text;
        },
        dateString: async function(content) {
            let theDay = content.getDate().toString();
            if (theDay.length == 1) theDay = `0${theDay}`;
            let theMonth = (content.getMonth() + 1).toString();
            if (theMonth.length == 1) theMonth = `0${theMonth}`;
            const theYear = content.getFullYear().toString();
            return `${theYear}-${theMonth}-${theDay}`;
        },
        toc: async function(content) {
            const htmlTagsFound = libdocUtils.extractHtmlTagsFromString(content, libdocConfig.tocHtmlTags);
            let tocMarkup = '';
            if (htmlTagsFound.length > libdocConfig.tocMinTags) {
                tocMarkup = `
                    <ol class="cgap-3em | m-0 pl-0 pb-5 o-auto | lh-1 | ls-none bwidth-1 bstyle-dashed bcolor-neutral-500 btwidth-0 brwidth-0"
                        d-flex="xs,sm"
                        fd-column="xs,sm"
                        fw-wrap="xs,sm"
                        columns-3="md"
                        columns-2="sm"
                        maxh-300px="sm"
                        maxh-200px="xs">`;
                // Displaying the results
                const anchorsIds = [];
                htmlTagsFound.forEach(function(htmlTag, tagIndex) {
                    let slugifiedId = libdocUtils.slugify(htmlTag.value);
                    if (anchorsIds.includes(slugifiedId)) {
                        slugifiedId += `-${tagIndex}`;
                    }
                    anchorsIds.push(slugifiedId);
                    const invalidFirstCharacters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
                    if (invalidFirstCharacters.includes(slugifiedId[0])) slugifiedId = 'a_' + slugifiedId;
                    tocMarkup += `
                        <li class="d-flex">
                            <a  href="#${slugifiedId}"
                                class="pl-5 pt-1 pb-1 | fs-4 lsp-3 lh-5 fvs-wght-400 wb-break-word | blwidth-1 blstyle-dashed bcolor-neutral-500">
                                ${htmlTag.value}
                            </a>
                        </li>`;
                });
                tocMarkup += '</ol>';
            }
            return tocMarkup;
        },
        gitLastModifiedDate: async function(filePath) {
            // Run the git log command
            // https://jamesdoc.com/blog/2023/git-changelog-in-11ty/
            let fileHistory = childProcess
                .execSync(`git log --pretty=tformat:"%cs" ${filePath}`)
                .toString()
                .trim();

            // If the file isn't committed to git then ignore
            if (fileHistory == "") { return false }

            return fileHistory.split(/\r?\n/)[0];
        }
    },
    collections: {
        myTags: function(collectionsApi) {
            const allData = collectionsApi.getAll();
            let unsortedTagsCount = {};
            allData.forEach(function(item) {
                if (typeof item.data.tags == 'object') {
                    item.data.tags.forEach(function(tag) {
                        if (tag !== 'post') {
                            if (unsortedTagsCount[tag] === undefined) {
                                unsortedTagsCount[tag] = 1
                            } else {
                                unsortedTagsCount[tag]++
                            }
                        }
                    })
                }
            });
            let sortedObject = Object.fromEntries(
                Object.entries(unsortedTagsCount).sort(([, a], [, b]) => b - a)
            );
            return Object.entries(sortedObject);
        },
        postsByDateDescending: function(collectionsApi) {
            return collectionsApi.getFilteredByTag("post").sort(function (a, b) {
                //return a.date - b.date; // sort by date - ascending
                return b.date - a.date; // sort by date - descending
                //return a.inputPath.localeCompare(b.inputPath); // sort by path - ascending
                //return b.inputPath.localeCompare(a.inputPath); // sort by path - descending
            });
        }
    },
    shortcodes: {
        alert: async function(content, type, title) {
            const validTypes = ['info', 'warning', 'success', 'danger'];
            let markup = '',
                titleAttribute = ``,
                typeClass = ``;
            if (typeof title == 'string') {
                titleAttribute = `data-title="${title}"`;
            }
            if (typeof type == 'string') {
                if (validTypes.includes(type)) typeClass = `alert-${type}`;
            }
            markup = `
                <aside class="widget widget-alert">
                    <div class="alert ${typeClass}" ${titleAttribute}>
                        ${content}
                    </div>
                </aside>
            `;
            return markup;
        },
        icon: async function(iconName, iconSize) {
            let markup = '';
            const fontSizeParse = parseInt(iconSize);
            const isSystemIcon = libdocSystem.icons.includes(iconName);
            let dsFontSize = '';
            if (!isNaN(fontSizeParse)) {
                if (fontSizeParse < 11 && fontSizeParse > 0) {
                    dsFontSize = fontSizeParse;
                }
            }
            if (isSystemIcon) {
                markup = `<span class="icon-${iconName} fs-${dsFontSize}"></span>`;
            } else {
                markup = `<span class="icon- fs-${dsFontSize}" style="mask-image: url('${libdocConfig.htmlBasePathPrefix}${iconName}')"></span>`;
            }
            return markup;
        },
        iconCard: async function(mainText, description, iconName) {
            let markup = '';
            if (typeof mainText == 'string' && typeof description == 'string') {
                const isSystemIcon = libdocSystem.icons.includes(iconName);
                let iconMarkup = ``;
                if (isSystemIcon) {
                    iconMarkup = `<span class="icon-${iconName} fs-10 | c-primary-500" fs-8="xs"></span>`;
                } else {
                    iconMarkup = `<span class="icon- fs-10 | c-primary-500"
                            fs-8="xs"
                            style="mask-image: url('${libdocConfig.htmlBasePathPrefix}${iconName || `/core/assets/icons/check-circle.svg`}')"></span>`;
                }
                markup = `
                    <aside class="widget widget-iconCard">
                        <p class="d-flex gap-5 | p-5 m-0 | brad-3 bwidth-1 bstyle-dashed bcolor-neutral-500">
                            ${iconMarkup}
                            <span class="d-flex fd-column gap-1">
                                <strong class="fvs-wght-700 fs-6">${mainText}</strong>
                                <span>${description}</span>
                            </span>
                        </p>
                    </aside>`;
            } else {
                console.log(`iconCard shortcode content: "${content}" wrong format, must specify at least main text and description string fields.`);
            }
            return markup;
        },
        embed: async function(src, height) {
            try {
                const url = new URL(src);
                const content = `
                    <aside class="widget widget-embed">
                        <iframe src="${url}"
                            frameborder="0"
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                            loading="lazy"
                            height="${height || ``}"
                            allowfullscreen></iframe>
                    </aside>`;
                return content;
            } catch (e) {
                console.log(`${src} is not a valid URL`);
                return '';
            }
        },
        icons: async function() {
            let markup = `
                <aside class="widget widget-icons | mt-10 mb-10"
                    mt-7="xs"
                    mb-7="xs">
                    <ul class="d-flex fw-wrap gap-7 | p-0 | ls-none" rgap-10="sm,md">`;
            libdocSystem.icons.forEach(function(iconName) {
                markup += `
                    <li class="d-flex fd-column ai-center gap-3" style="width: 20%">
                        <span class="icon-${iconName} fs-10"></span>
                        <code class="fs-2 tws-balance ta-center" fs-1="xs">${iconName}</code>
                    </li>`;
            });
            markup += '</ul></aside>';
            return markup;
        },
        sandbox: async function(content, sandboxTitle) {
            const   code = libdocUtils.HTMLEncode(content.replace(/[\n\r]/, '')),
                    title = typeof sandboxTitle == `string` ? sandboxTitle : libdocMessages.sandbox[libdocConfig.lang],
                    iframeAttribute = `srcdoc="${code}"`,
                    enableSwitchId = libdocUtils.generateRandomId(),
                    iframeCommands = `<header class="d-flex jc-space-between | pl-5" style="height: 58px">
                            <div class="d-flex ai-center | fvs-wght-400 fs-3 | c-neutral-500">
                                srcdoc
                            </div>
                        </header>`;
            return libdocUtils.templates.sandbox({iframeAttribute, iframeCommands, title, code, enableSwitchId});
        },
        sandboxFile: async function(content, permalink, sandboxTitle) {
            const   code = libdocUtils.HTMLEncode(content),
                    iframeAttribute = `src="${permalink}"`,
                    title = typeof sandboxTitle == `string` ? sandboxTitle : libdocMessages.sandbox[libdocConfig.lang],
                    enableSwitchId = libdocUtils.generateRandomId(),
                    iframeCommands = `<header class="d-flex jc-space-between gap-5 | pl-5 pr-5" style="height: 58px">
                            <a  href="${permalink}"
                                target="_blank"
                                title="${libdocMessages.openInANewTab[libdocConfig.lang]}"
                                class="d-flex ai-center gap-1 | p-0 | fvs-wght-400 fs-2 tt-uppercase td-none | sandbox__permalink"
                                fs-2="xs">
                                <span class="fvs-wght-400">${libdocMessages.open[libdocConfig.lang]}</span>
                                <span class="icon-arrow-square-out"></span>
                            </a>
                            <div class="d-flex gap-7">
                                <button type="button"
                                    class="d-flex ai-center | p-0 | fvs-wght-400 fs-2 tt-uppercase | bc-0 b-0 cur-pointer | sandbox__reload">
                                    <span class="o-hidden | to-ellipsis ws-nowrap">${libdocMessages.reload[libdocConfig.lang]}</span>
                                </button>
                                <button type="button"
                                    class="d-flex ai-center | p-0 | fvs-wght-400 fs-2 tt-uppercase | bc-0 b-0 cur-pointer | sandbox__copy_url">
                                    <span class="o-hidden | to-ellipsis ws-nowrap">${libdocMessages.copyURL[libdocConfig.lang]}</span>
                                </button>
                            </div>
                        </header>`;
            return libdocUtils.templates.sandbox({iframeAttribute, iframeCommands, title, code, enableSwitchId});
        }
    }
}