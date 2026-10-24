---
title: Met.no
description: Configure the Met.no weather provider.
layout: libdoc_page.liquid
permalink: weather/met-no/index.html
tags:
    - weather
eleventyNavigation:
    key: Met.no
    parent: Weather
    order: 5
---

Met.no's [Terms of Service](https://api.met.no/doc/TermsOfService) requires you to identify yourself. The purpose is to ensure they can contact you in case you overload or abuse their servers. For this reason, you just need to set your email address in `config.toml`:

```toml
[weather.providers.metno]
self_identification = "you@example.com"
```

Note that the Met.no API provides 6 hours of forecast, rather than a full day.
