---
title: Met Éireann (Ireland)
description: Configure the Met Éireann severe weather warning provider.
layout: libdoc_page.liquid
permalink: alerts/met-eireann/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts - Met Éireann (Ireland)
    parent: Alerts
    order: 4
---

To use alerts from Met Éireann, visit https://www.met.ie/Open_Data/json/ and choose the appropriate "warning_EIXX" JSON file for your region, using each county's FIPS code. This code can be found in the table on http://www.statoids.com/uie.html, in the pre-2014 section. For example, this is the file for Dublin:

```toml
[alerts.providers.met_eireann]
feed_url = "https://www.met.ie/Open_Data/json/warning_EI07.json"
```
