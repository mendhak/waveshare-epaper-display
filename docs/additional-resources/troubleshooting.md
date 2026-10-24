---
title: Troubleshooting
description: Common problems and clearing cached data.
layout: libdoc_page.liquid
permalink: additional-resources/troubleshooting/index.html
tags:
    - troubleshooting
eleventyNavigation:
    key: Troubleshooting
    parent: Additional Resources
    order: 1
---


### Scripts not working

If the scripts don't work at all, try going through the [Waveshare sample code](/additional-resources/waveshare-resources/) - if you can get those working, this script should work for you too.

You may want to further troubleshoot if you're seeing or not seeing something expected. If you've set up the cron job as shown in [Automate it](/running/automate/), a `run.log` file will appear which contains some info and errors. If there isn't enough information in there, you can set the log level in `config.toml`:

```toml
[locale]
log_level = "DEBUG"
```

### Caching

The scripts cache the calendar and weather information, to avoid hitting weather API rate limits. All temporary files are stored in the `data/` folder.

If you want to force a weather update, delete `data/cache_weather.json`.  
If you want to force a calendar update, delete `data/cache_all_calendars.pickle`.  
If you want to force a re-login to Google or Outlook, delete `data/token_google.pickle` or `data/token_outlook.bin`.  

To clear all cached data at once, run: `rm -rf data/*`
