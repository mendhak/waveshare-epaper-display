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

{% alert 'Met.no API provides 6 hours of forecast, rather than a full day.', 'info', 'Note' %}

Met.no's [Terms of Service](https://api.met.no/doc/TermsOfService) requires you to identify yourself. The purpose is to ensure they can contact you in case you overload or abuse their servers. For this reason, you just need to set your email address in `config.toml`:

In `config.toml`, choose to use the Met.no provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "metno"
```

Then add a section for the Met.no provider with your self-identification email.

```toml
[weather.providers.metno]
self_identification = "you@example.com"
```


