---
title: SMHI (Sweden)
description: Configure the SMHI weather provider.
layout: libdoc_page.liquid
permalink: weather/smhi/index.html
tags:
    - weather
eleventyNavigation:
    key: SMHI (Sweden)
    parent: Weather
    order: 10
---

SMHI requires you to identify yourself. 

In `config.toml`, choose to use the SMHI provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "smhi"
```

Then add a section for the SMHI provider with your self-identification:

```toml
[weather.providers.smhi]
self_identification = "you@example.com"
```
