---
title: Weather.gov (US)
description: Configure the Weather.gov severe weather warning provider.
layout: libdoc_page.liquid
permalink: alerts/weathergov/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts - Weather.gov (US)
    parent: Alerts
    order: 3
---

Weather.gov requires you to [identify your application](https://www.weather.gov/documentation/services-web-api). This can be any made up string, or an email address.

In `config.toml`, set your identifier:

```toml
[alerts.providers.weathergov]
self_identification = "you@example.com"
```

This provider will use the same latitude and longitude as specified for the weather provider.

> [!WARNING]
> YMMV. During testing, the weather.gov API was found to start returning errors and then suddenly work again.
