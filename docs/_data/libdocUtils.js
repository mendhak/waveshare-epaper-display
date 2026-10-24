// START IMPORT REQUIRE WORKAROUND
// To make 11ty --serve work with JSON imports
// https://github.com/11ty/eleventy/issues/3128#issuecomment-1878745864
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
// END IMPORT REQUIRE WORKAROUND

// START JSON IMPORT WORKAROUND
// import libdocMessages from "./libdocMessages.json" with { "type": "json" };
// import libdocPackage from "../package.json" with { "type": "json" };
const libdocMessages = require("./libdocMessages.json");
const libdocPackage = require("../package.json");
// END JSON IMPORT WORKAROUND

import libdocConfig from "./libdocConfig.js";

export default {
    version: function() {
        return libdocPackage.version
    },
    // environment: process.env.MY_ENVIRONMENT || "development",
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
    slugify: function(str) {
        // https://jasonwatmore.com/vanilla-js-slugify-a-string-in-javascript
        // make lower case and trim
        let slug = str.toLowerCase().trim();
        // remove accents from charaters
        slug = slug.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        // replace invalid chars with spaces
        slug = slug.replace(/[^a-z0-9\s-]/g, ' ').trim();
        // replace multiple spaces or hyphens with a single hyphen
        slug = slug.replace(/[\s-]+/g, '-');
        return slug;
    },
    extractHtmlTagsFromString: function(string, htmlTagsListArray) {
        // https://stackoverflow.com/a/65725198
        const htmlTagsFound = [];
        string.replace(/<([a-zA-Z][a-zA-Z0-9_-]*)\b[^>]*>(.*?)<\/\1>/g, function(m,m1,m2) {
            if (htmlTagsListArray.includes(m1)) {
                // write data to result object
                htmlTagsFound.push({
                    tagName: m1,
                    value: m2
                });
            }
        });
        return htmlTagsFound
    },
    generateRandomId: function(length) {
        const charactersList = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let id = '';
        if (typeof length != 'number') length = 8;
        for (let index = 0; index < length; index++) {
            const randomIndex = Math.floor(Math.random() * charactersList.length);
            id += charactersList[randomIndex];
        }
        return id;
    },
    templates: {
        sandbox: function({iframeAttribute, iframeCommands, title, code, enableSwitchId}) {
            return `
                <aside class="d-flex | sandbox"
                    fd-column="xs,sm"
                    gap-2="xs,sm"
                    ai-start="xs,sm"
                    o-hidden="md"
                    pl-9="md"
                    pr-9="md"
                    pl-5="xs,sm"
                    pr-5="xs,sm">
                    <div class="d-flex | p-1 o-hidden | brad-2 | sandbox__tabs"
                        d-none="md">
                        <button type="button"
                            class="d-flex | pt-2 pb-2 pl-5 pr-5 | fvs-wght-400 fs-2 tt-uppercase | b-0 brad-1 cur-pointer | sandbox__tab"
                            data-name="code">
                            ${libdocMessages.code[libdocConfig.lang]}
                        </button>
                        <button type="button"
                            class="d-flex | pt-2 pb-2 pl-5 pr-5 | fvs-wght-400 fs-2 tt-uppercase | b-0 brad-1 cur-pointer | sandbox__tab __active"
                            data-name="iframe">
                            ${libdocMessages.result[libdocConfig.lang]}
                        </button>
                    </div>
                    <div class="d-flex fd-column d-none--xs d-none--sm | o-hidden | brad-3 | sandbox__code_wrapper"
                        w-50="md"
                        w-100="xs,sm"
                        bradtr-0="md"
                        bradbr-0="md">
                        <header class="d-flex jc-space-between | pl-5" style="height: 58px">
                            <p class="d-flex ai-center | m-0 | fvs-wght-400 fs-3 lh-1"
                                fs-2="xs">
                                ${title}
                            </p>
                            <button type="button"
                                class="d-flex ai-center | pl-5 pr-5 | fvs-wght-400 fs-2 tt-uppercase | bc-0 b-0 cur-pointer | sandbox__copy_code"
                                title="${libdocMessages.copyHTML[libdocConfig.lang]}">
                                <span class="o-hidden | to-ellipsis ws-nowrap">${libdocMessages.copy[libdocConfig.lang]}</span>
                            </button>
                        </header>
                        <div class="pos-relative"
                            pl-5="md">
                            <pre class="m-0 h-500px o-auto"
                                bradtl-3="md"
                                bradbl-3="md">
                                <code class="language-html fvs-mono-on fvs-wght-300 fs-3 lh-6 | sandbox__code" fs-2="xs">${code}</code>
                            </pre>
                            <div class="d-flex jc-center ai-center | pos-absolute top-0 left-0 | w-100 h-100 | sandbox__enable_wrapper"
                                style="background-color: rgba(0,0,0,0.5)">
                                <input type="checkbox"
                                    id="${enableSwitchId}_code"
                                    value=""
                                    class="pos-absolute | opa-0 | sandbox__enable_switch"
                                    ${libdocConfig.sandboxRunSwitch ? `` : `checked`}>
                                <label for="${enableSwitchId}_code"
                                    class="d-flex ai-center gap-1 | p-5 | fvs-wght-500 tt-uppercase | bc-neutral-900 brad-2 cur-pointer">
                                    <span class="icon-play"></span>
                                    ${libdocMessages.enable[libdocConfig.lang]}
                                </label>
                            </div>
                        </div>
                        <div class="d-flex gap-2 | m-0 pt-1 pb-1 pl-0 | fvs-wght-400 fs-2 lh-1 | ls-none"
                            pl-2="xs,sm">
                            &nbsp;
                        </div>
                    </div>
                    <button class="pos-relative | p-0 | b-0 | sandbox__resizer"
                        title="${libdocMessages.sandboxResizeHelper[libdocConfig.lang]}"
                        d-none="xs,sm">
                        <span class="icon-dots-six-vertical fs-5"></span>
                    </button>
                    <div class="d-flex fd-column | pos-relative | o-hidden | brad-3 | sandbox__iframe_wrapper"
                        w-50="md"
                        w-100="xs,sm"
                        bradtl-0="md"
                        bradbl-0="md"
                        style="box-sizing: content-box">${iframeCommands}
                        <div class="d-flex | pos-relative">
                            <iframe ${iframeAttribute} loading="lazy" class="w-100 h-500px | b-0 | sandbox__iframe" style="background:white"></iframe>
                            <div class="d-flex jc-center ai-center | pos-absolute top-0 left-0 | w-100 h-100 | sandbox__enable_wrapper"
                                style="background-color: rgba(0,0,0,0.5)">
                                <input type="checkbox"
                                    id="${enableSwitchId}_iframe"
                                    value=""
                                    class="pos-absolute | opa-0 | sandbox__enable_switch"
                                    ${libdocConfig.sandboxRunSwitch ? `` : `checked`}>
                                <label for="${enableSwitchId}_iframe"
                                    class="d-flex ai-center gap-1 | p-5 | fvs-wght-500 tt-uppercase | bc-neutral-900 brad-2 cur-pointer">
                                    <span class="icon-play"></span> ${libdocMessages.enable[libdocConfig.lang]}
                                </label>
                            </div>
                        </div>
                        <ul class="d-flex gap-2 | m-0 pt-1 pb-1 pl-2 | fvs-wght-400 fs-2 lh-1 | ls-none">
                            <li>${libdocMessages.width[libdocConfig.lang]}: <span class="sandbox__monitor__iframe_width">-</span>px</li>
                            <li>${libdocMessages.height[libdocConfig.lang]}: <span class="sandbox__monitor__iframe_height">-</span>px</li>
                        </ul>
                    </div>
                </aside>`;
        }
    }
};