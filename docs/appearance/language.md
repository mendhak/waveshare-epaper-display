---
title: Display language
description: Install and force a different display language / locale.
layout: libdoc_page.liquid
permalink: appearance/language/index.html
tags:
    - appearance
eleventyNavigation:
    key: Display language
    parent: Appearance
    order: 1
---

The default locale of the system will be used to generate the time and date formats, including month and day names. On Raspberry Pi OS the default is usually `en_GB`.

To see the current default locale, run `locale`. To see all the locales installed on the system, use `locale -a`.

To install a new locale, go through the locale wizard:

```bash
sudo dpkg-reconfigure locales
```

Select the locales you want to install, be sure to pick the ones that have `.UTF-8` in the name.

In `config.toml`, set the language under `[locale]`:

```toml
[locale]
language = "ko_KR.UTF-8"
```

The next time `run.sh` runs, the output should have the chosen language.

### Fonts for non-western languages

Some languages may not render well because the default Raspberry Pi system fonts don't have all the characters needed to display on screen. For such cases, you'll need to find and install a font that supports all the characters you want to display.

Chinese/Japanese/Korean should already be taken care of by installing the `fonts-noto` package. But sometimes just installing that isn't enough, you'll also have to set it as the default font, see the [font instructions](/appearance/font/).

The reason this is necessary: the SVG renderer [does not support fallback fonts](https://github.com/Kozea/CairoSVG/issues/72#issuecomment-132500219) which means that if a font doesn't have a certain character, it won't ask the system for other fonts to help plug the gaps. You'll just see squares.
