---
title: Weather.gov (US)
description: Configure the Weather.gov weather provider.
layout: libdoc_page.liquid
permalink: weather/weathergov/index.html
tags:
    - weather
eleventyNavigation:
    key: Weather.gov (US)
    parent: Weather
    order: 7
---

Weather.gov requires you to [identify your application](https://www.weather.gov/documentation/services-web-api). This can be any made up string, or an email address.

In `config.toml`, set your identifier:

```toml
[weather.providers.weathergov]
self_identification = "you@example.com"
```

> [!WARNING]
> YMMV. During testing, the weather.gov API was found to start returning errors and then suddenly work again.
