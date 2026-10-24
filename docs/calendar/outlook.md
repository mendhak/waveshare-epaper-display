---
title: Outlook Calendar
description:
layout: libdoc_page.liquid
permalink: calendar/outlook/index.html
tags:
    - calendar
eleventyNavigation:
    key: Outlook Calendar
    parent: Calendar
    order: 3
---

The setup is much simpler than Google calendar, just run this script which will give instructions on how to login:

```bash
.venv/bin/python3 utils/outlook_util.py
```

Login with the Microsoft account you want to get the calendar from, and accept the consent screen. 

After a moment, the script will then display a set of Calendar IDs and some sample events from those Calendars. 

Copy the ID of the calendar you want, and add it to `config.toml`:

```toml
[[calendar.providers.outlook]]
enabled = true
calendar_id = "AQMkAxyz..."
```

To add multiple Outlook calendars, include additional `[[calendar.providers.outlook]]` blocks.
