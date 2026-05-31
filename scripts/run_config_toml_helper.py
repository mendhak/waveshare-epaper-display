#! /usr/bin/env python3
import tomllib

config = tomllib.load(open("config.toml", "rb"))
disp = config.get("display", {})
priv = config.get("privacy", {})
loc = config.get("locale", {})

print(f'export WAVESHARE_EPD75_VERSION="{disp.get("waveshare_version", "2")}"')
print(f'export SCREEN_LAYOUT={disp.get("screen_output_layout", 1)}')

privacy_enabled = priv.get("enabled", False)
privacy_mode = priv.get("mode", "literature")  # default: literature

print(f'export PRIVACY_ENABLED={1 if privacy_enabled else 0}')
print(f'export PRIVACY_MODE="{privacy_mode}"')
print(f'export LANG="{loc.get("language", "")}"')
