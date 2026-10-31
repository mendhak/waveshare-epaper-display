---
title: Climacell (tomorrow.io)
description: Configure the Climacell (tomorrow.io) weather provider.
layout: libdoc_page.liquid
permalink: weather/climacell/index.html
tags:
    - weather
eleventyNavigation:
    key: Climacell (tomorrow.io)
    parent: Weather
    order: 8
---

Register on the [Climacell site](https://www.climacell.co/weather-api/), and when you do you should be given an API Key.

In `config.toml`, choose to use the Climacell provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "climacell"
```

Then add a section for the Climacell provider with your API key:

```toml
[weather.providers.climacell]
api_key = "xxxxxx"
```
