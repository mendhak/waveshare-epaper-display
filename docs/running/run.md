---
title: Run it
description: Run the script to render and display a frame.
layout: libdoc_page.liquid
permalink: running/run/index.html
tags:
    - running
eleventyNavigation:
    key: Run it
    parent: Running
    order: 1
---

Run `./run.sh` which should query the weather provider and Google/Outlook Calendar. It will then create a png, convert to a 1-bit black and white bmp, then display the bmp on screen.

Using a 1-bit, low grade BMP is what allows the screen to refresh relatively quickly. Calling the BCM code to do it takes about 6 seconds. Rendering a high quality PNG or JPG and rendering to screen with Python takes about 35 seconds.

Once you've proven that the run works, and an image is sent to your epaper display, see [Automate it](/running/automate/) to run it on a schedule.
