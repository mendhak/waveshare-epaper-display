---
title: Automate it
description: Run the display automatically with cron or a systemd timer.
layout: libdoc_page.liquid
permalink: running/automate/index.html
tags:
    - running
eleventyNavigation:
    key: Automate it
    parent: Running
    order: 2
---

## Cron

Once you've proven that the run works, and an image is sent to your epaper display, you can automate it by setting up a cronjob.

```bash
crontab -e
```

Add this entry so it runs every minute:

```cron
* * * * * cd /home/pi/waveshare-epaper-display && bash run.sh > run.log 2>&1
```

This will cause the script to run every minute, and write the output as well as errors to the run.log file.

## systemd timer

Alternatively, you can use a systemd timer. There are example systemd units available to install a timer that starts a service every minute that runs the script. To achieve this, execute the following commands.

```bash
mkdir -p ~/.config/systemd/user/
cp utils/waveshare_epaper_display.service.example ~/.config/systemd/user/waveshare_epaper_display.service
cp utils/waveshare_epaper_display.timer.example ~/.config/systemd/user/waveshare_epaper_display.timer
systemctl --user daemon-reload
systemctl --user enable waveshare_epaper_display.timer
loginctl enable-linger
```
