---
title: Met Éireann (Ireland)
description: 
layout: libdoc_page.liquid
permalink: alerts/met-eireann/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts - Met Éireann (Ireland)
    parent: Alerts
    order: 4
---

To use alerts from Met Éireann, visit [https://www.met.ie/Open_Data/json/](https://www.met.ie/Open_Data/json/) and choose the appropriate `warning_EIXX` JSON file for your region, using each county's [FIPS code](https://statoids.com/uie.html). 


In `config.toml`, set the `[alerts]` section as follows:

```toml
[alerts]
enabled = true
provider = "met_eireann"
```

Then add a section for the Met Éireann provider with the feed URL. For example, this is the configuration for Dublin:

```toml
[alerts.providers.met_eireann]
feed_url = "https://www.met.ie/Open_Data/json/warning_EI07.json"
```
