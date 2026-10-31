---
title: CalDav Calendar
description: 
layout: libdoc_page.liquid
permalink: calendar/caldav/index.html
tags:
    - calendar
eleventyNavigation:
    key: CalDav Calendar
    parent: Calendar
    order: 5
---

{% alert, "Some CalDav features may not work well as the protocol is heavily undocumented, proprietary, and many servers don't implement it the same way.", "warning" %}

For CalDav you will need the CalDav URL, username, and password. Add them to `config.toml`:

```toml
[[calendar.providers.caldav]]
enabled = true
url = "https://nextcloud.example.com/remote.php/dav/principals/users/123456/"
username = "username"
password = "password"
id = "your-calendar-id"
```


To add multiple CalDav calendars, include additional `[[calendar.providers.caldav]]` blocks.
