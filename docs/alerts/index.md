---
title: Choosing a severe weather warning provider
description: Optionally display severe weather warnings on the screen.
layout: libdoc_page.liquid
permalink: alerts/index.html
tags:
    - alerts
eleventyNavigation:
    key: Alerts
    order: 4
---
{% alert 'This is an optional step. By doing nothing you will not see severe weather warnings.', 'info', 'Optional' %}

In `config.toml`, set `enabled` to true, and the `provider` name you wish to use under `[alerts]`:

```toml
[alerts]
enabled = true
provider = "metoffice" # metoffice, met_eireann, weathergov
```

Then configure the corresponding provider below:

* [Met Office (UK)](/alerts/met-office/)
* [Weather.gov (US)](/alerts/weathergov/)
* [Met Éireann (Ireland)](/alerts/met-eireann/)
