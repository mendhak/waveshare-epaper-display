---
title: Debugging locally
description: Run and debug the application on your local machine.
layout: libdoc_page.liquid
permalink: additional-resources/local-development/index.html
tags:
    - development
eleventyNavigation:
    key: Debugging locally
    parent: Additional Resources
    order: 3
---

It's possible to run and debug the application locally with virtual environments. The last step fails, as it's trying to write to GPIO, but that's not an issue since the aim of local development is to generate and view the `data/screen_output.png`.

Do this before opening VSCode:

```bash
# Generate the virtual environment directory
python3 -m venv .venv
# Switch to it
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

Then, open VSCode with the project, and it should automatically detect and switch to the virtual environment in the terminal.

Copy `config.example.toml` to `config.toml` and configure your settings.

To run the project, just run `./run.sh`. It will read config.toml and run the various Python scripts.

To debug the project, open a Python script file such as `scripts/screen_calendar_get.py` or `scripts/screen_weather_get.py`, and press F5. It will use config.toml for settings and run the script. It can hit breakpoints, no problem.
