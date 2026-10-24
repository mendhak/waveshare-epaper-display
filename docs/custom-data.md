---
title: Custom data
description: Add your own custom data (Home Assistant, PiHole, API calls) to the screen.
layout: libdoc_page.liquid
permalink: custom-data/index.html
tags:
    - custom-data
eleventyNavigation:
    key: Custom data
    order: 9
---

This is an optional step, to add your own custom data to the screen. For example this could be API calls, data from Home Assistant, PiHole stats, or something external.

Rename `scripts/screen_custom_get.py.sample` to `scripts/screen_custom_get.py`. Do your custom code, and set the value of `custom_value_1` to the value you want to display. Run `./run.sh` and it'll appear on screen.

Next, modify `templates/screen_custom.svg` and change the various x, y, font size values to adjust its appearance and position. You can add more values by adding more SVG elements for custom_value_2, custom_value_3, and so on, and set its value in the `output_dict` in `scripts/screen_custom_get.py`.
