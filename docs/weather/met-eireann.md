---
title: Met Éireann (Ireland)
description: Configure the Met Éireann weather provider.
layout: libdoc_page.liquid
permalink: weather/met-eireann/index.html
tags:
    - weather
eleventyNavigation:
    key: Met Éireann (Ireland)
    parent: Weather
    order: 6
---


[Met Éireann](https://www.met.ie/) publish their forecast data under a [Creative Commons Attribution 4.0 International license (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). No API key required.

In `config.toml`, just set the provider:

```ini
[weather]
... your location details from the location step ...
provider = "met_eireann"
```


{% alert 'The [terms](https://data.gov.ie/en_GB/dataset/met-eireann-forecast-api) of using the Met Éireann data is that their [weather alerts](/alerts/met-eireann/) must also be displayed.', 'info', 'Note' %}
