---
title: Layout
description: Choose your screen layout from these examples
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

In `config.toml`, set the layout under `[display]`. 

### `screen_output_layout = "1"`

```toml
[display]
screen_output_layout = "1"
```

This is the default layout.

![Layout 1](/screenshots/001.png)


### `screen_output_layout = "2"`
```toml
[display]
screen_output_layout = "2"
```
Shows more calendar entries and less emphasis on weather and time.

![Layout 2](/screenshots/002.png)

### `screen_output_layout = "3"`

```toml
[display]
screen_output_layout = "3"
```

Shows calendar entries on the left and less emphasis on weather.

![Layout 3](/screenshots/003.png)

### `screen_output_layout = "4"`

```toml
[display]
screen_output_layout = "4"
```

Shows the hour instead of the time and is meant for color screens that take a long time to refresh.

![Layout 4](/screenshots/004.png)

### `screen_output_layout = "5"`

```toml
[display]
screen_output_layout = "5"
```

Has calendar entries on the left, with a month calendar for at-a-glance viewing.

![Layout 5](/screenshots/005.png)
