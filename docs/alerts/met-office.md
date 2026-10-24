---
title: Met Office (UK)
description: 
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

In `config.toml`, set the `[alerts]` section as follows:

```toml
[alerts]
enabled = true
provider = "metoffice" 
```

Then add a section for the Met Office provider with the feed URL:

```toml
[alerts.providers.metoffice]
feed_url = "https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/se"
```
