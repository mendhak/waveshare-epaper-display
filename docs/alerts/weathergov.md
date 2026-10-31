---
title: Weather.gov (US)
description: 
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

In `config.toml`, set the `[alerts]` section as follows:

```toml
[alerts]
enabled = true
provider = "weathergov"
```

Then add a section for the Weather.gov provider with your self-identification:

```toml
[alerts.providers.weathergov]
self_identification = "you@example.com"
```

This provider will use the same latitude and longitude as specified for the weather provider.

{% alert '<abbr title="Your Mileage May Vary">YMMV</abbr>! During testing, the weather.gov API has been found to start returning errors, and then suddenly work again.', 'warning', 'Note' %}

