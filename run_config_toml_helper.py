#! /usr/bin/env python3
import tomllib, shlex

config = tomllib.load(open("config.toml", "rb"))
disp = config["display"]
priv = config["privacy"]

print(f'export WAVESHARE_EPD75_VERSION="{disp["waveshare_version"]}"')
print(f'export SCREEN_LAYOUT={disp["screen_output_layout"]}')
print(f'export PRIVACY_MODE_XKCD={1 if priv["xkcd"] else 0}')
print(f'export PRIVACY_MODE_LITERATURE_CLOCK={1 if priv["literature_clock"] else 0}')
