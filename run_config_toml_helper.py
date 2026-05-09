#! /usr/bin/env python3
import tomllib

config = tomllib.load(open("config.toml", "rb"))
disp = config.get("display", {})
priv = config.get("privacy", {})
loc = config.get("locale", {})

print(f'export WAVESHARE_EPD75_VERSION="{disp.get("waveshare_version", "2")}"')
print(f'export SCREEN_LAYOUT={disp.get("screen_output_layout", 1)}')
print(f'export PRIVACY_MODE_XKCD={1 if priv.get("xkcd", False) else 0}')
print(f'export PRIVACY_MODE_LITERATURE_CLOCK={1 if priv.get("literature_clock", False) else 0}')
print(f'export LANG="{loc.get("language", "")}"')
