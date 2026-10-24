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

```toml
[weather]
provider = "met_eireann"
```

Note that a condition of use of this data is that weather alerts also be displayed, so you should configure the Met Éireann alert provider under [Alerts](/alerts/met-eireann/).
