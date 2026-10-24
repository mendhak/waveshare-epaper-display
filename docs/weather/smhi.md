---
title: SMHI (Sweden)
description: Configure the SMHI weather provider.
layout: libdoc_page.liquid
permalink: weather/smhi/index.html
tags:
    - weather
eleventyNavigation:
    key: SMHI (Sweden)
    parent: Weather
    order: 10
---

SMHI requires you to identify yourself. Just set your own email in `config.toml`:

```toml
[weather.providers.smhi]
self_identification = "you@example.com"
```
