---
title: Location
description: Set your location and units.
layout: libdoc_page.liquid
permalink: configuration/location/index.html
tags:
    - configuration
eleventyNavigation:
    key: Location
    parent: Configuration
    order: 2
---

Whichever weather provider you use, you'll need to provide the location and units to display in. Where supported, these values will be passed to the weather provider. 

Edit `config.toml` and update the latitude and longitude under the `[weather]` section.

```toml
[weather]
latitude  = 51.5077
longitude = -0.1278
format = "CELSIUS"
```
