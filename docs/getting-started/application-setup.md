---
title: Application setup
description: Clone the repo, install dependencies, and create your config file.
layout: libdoc_page.liquid
permalink: getting-started/application-setup/index.html
tags:
    - getting-started
eleventyNavigation:
    key: Application setup
    parent: Getting Started
    order: 3
---

## Clone it

On the Raspberry Pi, clone this repository in the `/home/pi` directory.

```bash
cd ~
sudo apt update && sudo apt upgrade
sudo apt install git
git clone --recursive https://github.com/mendhak/waveshare-epaper-display.git
```

This should create a `/home/pi/waveshare-epaper-display` directory.

## Setup dependencies

```bash
cd waveshare-epaper-display
sudo apt install gsfonts fonts-noto python3 python3-pip libopenjp2-7 python3-venv libjpeg-dev libxslt1-dev fontconfig libcairo2
python3 -m venv --system-site-packages .venv
.venv/bin/pip3 install -r requirements.txt
sudo raspi-config nonint do_spi 0   # This enables SPI
sudo reboot
```

## Copy the config file

Copy the example config file to `config.toml`, this is where all the settings will be stored.

```bash
cd waveshare-epaper-display
cp config.example.toml config.toml
```

From here on, all settings live in `config.toml`. 
