---
title: Google Calendar
description: Configure the Google Calendar provider (requires a one-time OAuth flow).
layout: libdoc_page.liquid
permalink: calendar/google/index.html
tags:
    - calendar
eleventyNavigation:
    key: Google Calendar
    parent: Calendar
    order: 2
---

You will need to run an OAuth process once manually to allow this application to query your Google Calendar for information.

#### Get a token

Run:

```bash
.venv/bin/python3 utils/google_calendar_util.py
```

The script will prompt you to visit a URL in your browser, then it will sit there and wait. The URL will look like `https://accounts.google.com/o/...` and will be very long.

Follow that URL in a browser window, you'll need to log in and choose your Google account. On the "Make sure you trust Mendhak Waveshare Epaper Display" screen, you will see it's asking for permission to read your Google Calendar. Click continue, and then let it fail when it tries to go to a `http://localhost:8080/...` URL.

Copy the URL it was trying to go to (e.g. `http://localhost:8080/...`) and in another SSH session with the Raspberry Pi, run this (remember the double quotes):

```bash
curl "http://localhost:8080/..."
```

On the first screen you should see the auth flow complete, and a new `data/token_google.pickle` file appears. The script should now be able to run in the future without prompting required.

#### Get your calendar ID

The script will then print out a list of your Google Calendars with names and IDs. Copy the ID of the calendar you want, then add a section to `config.toml` to enable it, like this:

```toml
[[calendar.providers.google]]
enabled = true
id = "xyz12345@group.calendar.google.com"
time_zone = "Europe/London"  # Optional: for family calendars
```

To add multiple Google calendars, include additional `[[calendar.providers.google]]` blocks.

You can also get a calendar's ID manually by opening [Google Calendar](https://calendar.google.com) and going to the settings for your preferred calendar. Under the 'Integrate Calendar' section you will see a Calendar ID which looks like `xyz12345@group.calendar.google.com`.
