---
title: Climacell (tomorrow.io)
description: Configure the Climacell / tomorrow.io weather provider.
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

In `config.toml`, add your API key:

```toml
[weather.providers.climacell]
api_key = "xxxxxx"
```
