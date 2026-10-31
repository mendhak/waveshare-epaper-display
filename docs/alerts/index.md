---
title: Choose a severe weather warning provider
description: Display severe weather warnings/alerts on the screen.
layout: libdoc_page.liquid
permalink: alerts/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts
    order: 4
---

{% alert 'You can only choose one severe weather warning provider at a time.', 'info', 'Note' %}

This is an optional step. By doing nothing you will not see severe weather warnings/alerts.


You can choose between the following severe weather warning providers:

* [Met Office (UK)](/alerts/met-office/)
* [Weather.gov (US)](/alerts/weathergov/)
* [Met Éireann (Ireland)](/alerts/met-eireann/)

In each case, you will choose a provider under an `[alerts]` section, and then add another section for the specific provider.

Each provider is configured differently, please follow the instructions carefully for each provider.


### Example

```ini
[alerts]
enabled = true
provider = "metoffice" # metoffice, met_eireann, weathergov
```

Of course you can disable alerts by setting `enabled` to false. 
