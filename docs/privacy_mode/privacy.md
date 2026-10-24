---
title: Privacy mode
description: Hide the dashboard and show an XKCD comic or literature clock instead.
layout: libdoc_page.liquid
permalink: privacy/index.html
tags:
    - appearance
eleventyNavigation:
    key: Privacy mode
    order: 8
---

This mode hides away everything and just displays an XKCD comic or a literary quote for the time. In `config.toml`, enable privacy mode and select the mode:

```toml
[privacy]
enabled = true
mode = "xkcd"  # or "literature"
```

![XKCD](/screenshots/pvt_xkcd.png)


```toml
[privacy]
enabled = true
mode = "literature"
```

![Literature](/screenshots/pvt_literature.png)
