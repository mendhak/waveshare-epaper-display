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

In `config.toml`, choose to use the VisualCrossing provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "visualcrossing"
```

Then add a section for the VisualCrossing provider with your API key:


```toml
[weather.providers.visualcrossing]
api_key = "XXXXXXXXXXXXXXXXXXXXXX"
```
