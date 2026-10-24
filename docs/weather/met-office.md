---
title: Met Office (UK)
description: Configure the Met Office weather provider.
layout: libdoc_page.liquid
permalink: weather/met-office/index.html
tags:
    - weather
eleventyNavigation:
    key: Met Office (UK)
    parent: Weather
    order: 3
---

Create an account [on the Met Office Weather DataHub](https://datahub.metoffice.gov.uk) site.
Next, [under subscriptions](https://datahub.metoffice.gov.uk/profile/subscriptions) — subscribe to the 'Site Specific' product 'Global Spot'. This will get you an API key.

In `config.toml`, add your API key:

```toml
[weather.providers.metoffice]
api_key = "eyJ........."
```
