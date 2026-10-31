---
title: Run it
description:
layout: libdoc_page.liquid
permalink: running/run/index.html
tags:
    - running
eleventyNavigation:
    key: Run it
    parent: Running
    order: 1
---

Run the starter script:

```bash
./run.sh
```


This should query the weather provider, alert provider, and calendar. It will then create a png, convert to a 1-bit black and white bitmap, then display the bmp on screen.

Using a 1-bit, low grade BMP is what allows the screen to refresh relatively quickly. Rendering a high quality PNG or JPG and rendering to screen with Python takes about 35 seconds, which is why the low grade BMP approach is used.

Once you've proven that the run works, and an image is sent to your epaper display, see [Automate it](/running/automate/) to run it on a schedule.
