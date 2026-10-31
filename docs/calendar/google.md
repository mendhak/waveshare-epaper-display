---
title: Google Calendar
description: Configure the Google Calendar provider (requires a one-time login step).
layout: libdoc_page.liquid
permalink: calendar/google/index.html
tags:
    - calendar
eleventyNavigation:
    key: Google Calendar
    parent: Calendar
    order: 2
---

You will need to run a one-time, manual login step to allow this application to query your Google Calendar for information.

### Login step

Run:

```bash
.venv/bin/python3 utils/google_calendar_util.py
```

The script will prompt you to visit a URL in your browser, then it will sit there and wait. The URL will look like `https://accounts.google.com/o/...` and will be very long.

1. Follow that URL in a browser window
2. Log in and choose your Google account 
3. On the "_Make sure you trust Mendhak Waveshare Epaper Display_" screen, you will see it's asking for permission to read your Google Calendar. 
4. Click continue 
5. Let it fail when it tries to go to a `http://localhost:8080/...` URL


6. Copy the URL it was trying to go to (e.g. `http://localhost:8080/...`).  
7. In a _new_ SSH session with the Raspberry Pi, run the following (remember the double quotes):

```bash
curl "http://localhost:8080/..."
```

{% alert "No really, remember the double quotes around the URL. It catches most people out", "info" %}

Back on the first Raspberry Pi SSH screen you should see the auth flow complete, and a new `data/token_google.pickle` file appears. 

The script should now be able to run in the future without asking you to log in again.

### Get your calendar ID

The script will then print out a list of your Google Calendars with names and IDs. Copy the ID of the calendar you want.  

Then add a section to `config.toml` to enable it, like this:

```toml
[[calendar.providers.google]]
enabled = true
id = "xyz12345@group.calendar.google.com"
time_zone = "Europe/London"  # Optional: for family calendars
```

To add multiple Google calendars, you can include additional `[[calendar.providers.google]]` blocks.

```toml
[[calendar.providers.google]]
enabled = true
id = "another_calendar@group.calendar.google.com"
```

### How to get a calendar ID manually

You can also get a calendar's ID manually by opening [Google Calendar](https://calendar.google.com) and going to the settings for your preferred calendar. Under the 'Integrate Calendar' section you will see a Calendar ID which looks like `xyz12345@group.calendar.google.com`.

### How to clear the login

To clear the login, simply delete the `data/token_google.pickle` file.
