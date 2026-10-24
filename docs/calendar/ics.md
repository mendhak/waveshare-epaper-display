---
title: ICS Calendar
description: 
layout: libdoc_page.liquid
permalink: calendar/ics/index.html
tags:
    - calendar
eleventyNavigation:
    key: ICS Calendar
    parent: Calendar
    order: 4
---

ICS can be buggy. Get the ICS URL for a calendar, and add it to `config.toml`:

```toml
[[calendar.providers.ics]]
enabled = true
url = "https://calendar.google.com/calendar/ical/xxxxxxxxxxxx/xxxxxxxxxxxxxx/basic.ics"
```

There is no username/password support.

To add multiple ICS calendars, include additional `[[calendar.providers.ics]]` blocks.
