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

In `config.toml`, choose to use the Weather.gov provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "weathergov"
```


Then add a section for the Weather.gov provider with your self-identification:

```toml
[weather.providers.weathergov]
self_identification = "you@example.com"
```

{% alert '<abbr title="Your Mileage May Vary">YMMV</abbr>! During testing, the weather.gov API has been found to start returning errors, and then suddenly work again.', 'warning', 'Note' %}

