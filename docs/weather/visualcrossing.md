---
title: VisualCrossing
description: Configure the VisualCrossing weather provider.
layout: libdoc_page.liquid
permalink: weather/visualcrossing/index.html
tags:
    - weather
eleventyNavigation:
    key: VisualCrossing
    parent: Weather
    order: 9
---

Register on [VisualCrossing](https://www.visualcrossing.com/). Under Account Details, you should be able to generate an API key. Once you have that, add it to `config.toml`:

```toml
[weather.providers.visualcrossing]
api_key = "XXXXXXXXXXXXXXXXXXXXXX"
```
