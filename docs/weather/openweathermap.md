---
title: OpenWeatherMap
description: Configure the OpenWeatherMap weather provider.
layout: libdoc_page.liquid
permalink: weather/openweathermap/index.html
tags:
    - weather
eleventyNavigation:
    key: OpenWeatherMap
    parent: Weather
    order: 2
---

Register on the [OpenWeathermap](https://openweathermap.org) website, and go to the [API Keys page](https://home.openweathermap.org/api_keys) — that's the key you'll need.

In `config.toml`, choose to use the openweathermap provider. 

```toml
[weather]
... your location details from the location step ...
provider = "openweathermap"    
```


Then add a section for the openweathermap provider with your API key.

```toml
[weather.providers.openweathermap]
api_key = "xxxxxx"
```
