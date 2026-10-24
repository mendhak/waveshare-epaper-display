---
title: Met Office (UK)
description: Configure the Met Office severe weather warning provider.
layout: libdoc_page.liquid
permalink: alerts/met-office/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts - Met Office (UK)
    parent: Alerts
    order: 2
---

Go to the [Met Office RSS Feeds page](https://www.metoffice.gov.uk/weather/guides/rss) and copy the URL of the RSS feed based on your region.

In `config.toml`, add the feed URL:

```toml
[alerts.providers.metoffice]
feed_url = "https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se"
```
