---
title: Privacy mode
description: Hide the dashboard and show an XKCD comic or literature clock instead.
layout: libdoc_page.liquid
permalink: privacy/index.html
tags:
    - appearance
eleventyNavigation:
    key: Privacy mode
    order: 7
---

This mode hides away everything and just displays an XKCD comic or a literary quote for the time. I normally use this when I'm away on holiday or someone is visiting.

### Literature mode

This displays a literary quote for the current time, instead of the usual dashboard information.

```toml
[privacy]
enabled = true
mode = "literature"
```

![Literature](/screenshots/pvt_literature.png)


### XKCD mode

This displays a random XKCD comic, instead of the usual dashboard information. The image will often appear a bit stretched as XKCD comics aren't a fixed size.

In `config.toml`, enable privacy mode and select the mode:

```toml
[privacy]
enabled = true
mode = "xkcd"  # or "literature"
```

![XKCD](/screenshots/pvt_xkcd.png)


