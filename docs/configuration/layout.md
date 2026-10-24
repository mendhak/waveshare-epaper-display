---
title: Layout
description: Choose one of the available screen layouts.
layout: libdoc_page.liquid
permalink: configuration/layout/index.html
tags:
    - configuration
eleventyNavigation:
    key: Layout
    parent: Configuration
    order: 3
---

This is an optional step. There are a few different layouts to choose from.

In `config.toml`, set the layout under `[display]`:

```toml
[display]
screen_output_layout = "1"
```

| `screen_output_layout = "1"` <br />This is the default | `screen_output_layout = "2"` <br />More calendar entries and less emphasis on weather and time |
| --- | --- |
| [![Layout 1](/screenshots/001.png)](/screenshots/001.png) | [![Layout 2](/screenshots/002.png)](/screenshots/002.png) |

| `screen_output_layout = "3"` <br />Calendar entries on left, less emphasis on weather | `screen_output_layout = "4"` <br />Shows hour instead of time. Meant for color screens. |
| --- | --- |
| [![Layout 3](/screenshots/003.png)](/screenshots/003.png) | [![Layout 4](/screenshots/004.png)](/screenshots/004.png) |

| `screen_output_layout = "5"` <br />Calendar entries on left, with a month calendar for at-a-glance |  |
| --- | --- |
| [![Layout 5](/screenshots/005.png)](/screenshots/005.png) | |
