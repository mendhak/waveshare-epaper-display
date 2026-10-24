---
title: Hello Child 2
description: I am the second child page of hello page
layout: libdoc_page.liquid
eleventyNavigation:
    key: Hello Second Child
    parent: Hello Page
    order: 1
tags:
    - syntax-highlighting
    - blockquote
---
> Howdy! I am the second child page of hello page.
> 
> ― **Child**

Let’s go back to [hello page](/hello-page.md "Go back to hello page") or go to [hello grandchild](/hello-grandchild.md "Go to hello grandchild page").

```markdown
> Howdy! I am the second child page of hello page.
> 
> ― **Child**

Let’s go back to [hello page](/hello-page.md "Go back to hello page") or go to [hello grandchild](/hello-grandchild.md "Go to hello grandchild page").
```

### Clone it


1. git clone this repository in the /home/pi directory.
This should create a /home/pi/waveshare-epaper-display directory.

```
cd ~
sudo apt update && sudo apt upgrade
sudo apt install git
git clone --recursive https://github.com/mendhak/waveshare-epaper-display.git
```

### Setup dependencies

```
cd waveshare-epaper-display
sudo apt install gsfonts fonts-noto python3 python3-pip pigpio libopenjp2-7 python3-venv libjpeg-dev libxslt1-dev fontconfig libcairo2
python3 -m venv --system-site-packages .venv
.venv/bin/pip3 install -r requirements.txt
sudo raspi-config nonint do_spi 0  #This enables SPI
sudo reboot
```