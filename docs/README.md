# Eleventy LibDoc

[Eleventy LibDoc website](https://eleventy-libdoc.netlify.app/) | [11ty website](11ty)

Eleventy LibDoc is an easy to use and content focused starter project for [Eleventy][11ty] to craft slick and responsive documentation. It was was developed with accessibility awareness and low-tech mindset which allows to reach good page speed performances. It contains vanilla JS self-made components like search, primary navigation, table of content, code highlighting and sandboxes. Every page created with LibDoc is printable and can work properly even without Javascript by maintaining only essential features.

[![Netlify Status](https://api.netlify.com/api/v1/badges/d1986dbf-2272-4614-8dec-c228ba4699ef/deploy-status)](https://app.netlify.com/sites/11ty-libdoc-blank/deploys)

![LibDoc’s interface with both light and dark modes](https://github.com/user-attachments/assets/91e7eb6d-8089-40b7-94e4-4fd970073c8d)

<img width="1471" height="625" alt="image" src="https://github.com/user-attachments/assets/9af60d6f-8d5b-463e-9570-b5a6e54a8515" />
<img width="1461" height="617" alt="image" src="https://github.com/user-attachments/assets/f37bbe07-f65a-4a4f-acb1-6892ec202aac" />

> [!NOTE]
> Eleventy LibDoc is still under active development and therefore before reaching v1.0.0:
> * Full backward compatibility is not guaranteed.
> * Many features are subject to change.

## Getting started

1. Clone or fork <https://github.com/ita-design-system/eleventy-libdoc>
2. Run `npm install`
3. Enter your own settings in `settings.json`. [Configuration](https://eleventy-libdoc.netlify.app/configuration/).
4. Build `npx @11ty/eleventy --serve` or `npx @11ty/eleventy` (if you already have your own web server).

[View deployment of this repository](https://11ty-libdoc-blank.netlify.app)

## Update LibDoc

This process shows how to update Eleventy LibDoc Starter template.

> [!NOTE]
> As a starter template, any edit made into the following files and folders needs to be saved and pasted into the new version.
> **If edits were made into these files/folders, please save it and paste changes into the new version.**

1. Delete the following files and folders:
  * `_data`
  * `_includes`
  * `core`
  * `node_modules`
  * `.eleventy.js`
  * `package-lock.json`
  * `package.json`
2. Replace the same files and folders from the new Eleventy LibDoc version.
3. Run `npm install`, then you get the latest version. You can verify current version at the bottom of each page.

## Key features

* **Content focused** <br>LibDoc is easy to install, deploy and use.
* **Accessibility** <br>LibDoc was developed with accessibility awareness.
* **Performance** <br>Low front-end dependencies and vanilla JS self-made components make LibDoc cross-browser compatibility and good performances. <a href="https://developers.google.com/speed/pagespeed/insights/?url=eleventy-libdoc.netlify.app" target="_blank">View performances</a>.
* **Search** <br>Fuzzy and standard search modes. Keyboard shortcut 🆂 allows quick focus on search input field. Fuzzy search makes easy keyboard based navigation whereas standard search allows to find an exact match..
* **Smart navigation** <br>On page change, the primary navigation menu keeps its position.
* **Smart table of content** <br>In addition of a pure static table of content, LibDoc generates a floating <abbr title="Table of Content">TOC</abbr> always visible that also displays the current window scroll position.
* **Fallback if no Javascript available** <br>LibDoc can work even without Javascript with reduced features.
* **Image transcoding** <br>LibDoc transcodes and resizes your source images into production ready formats.
* **Printable** <br>Every page created with LibDoc can be printed.
* **Light and dark modes** <br>LibDoc’s interface is available with both light and dark mode color schemes.
* **Slick code highlighting** <br>Display your code in a nice style and adjust which code languages you really use.
* **Sandboxes** <br>Showcase small demos or full HTML pages into a responsive dual pane.
* **Atom feed** <br>The Atom feed allows visitors to subscribe to post blog content.

## Documentation

* [LibDoc’s homepage](https://eleventy-libdoc.netlify.app) <br>The website containing LibDocs’s presentation and comprehensive documentation.
    * [Configuration](https://eleventy-libdoc.netlify.app/configuration/) <br>List and descriptions of every LibDoc parameter.
    * [Creating content](https://eleventy-libdoc.netlify.app/creating-content/) <br>How LibDoc can display your content in multiple ways.
    * [Front matter](https://eleventy-libdoc.netlify.app/front-matter/) <br>Documentation of all front matter settings related to a LibDoc page.
    * [Primary navigation](https://eleventy-libdoc.netlify.app/primary-navigation/) <br>Detailed features of LibDoc’s primary navigation.
    * [SEO](https://eleventy-libdoc.netlify.app/configuration/seo/) <br>How LibDoc’s configuration and pages parameters are applied for Search Engine Optimization.
    * [Credits](https://eleventy-libdoc.netlify.app/configuration/credits/) <br>LibDoc could not work without these resources.

[11ty]: https://www.11ty.dev/
