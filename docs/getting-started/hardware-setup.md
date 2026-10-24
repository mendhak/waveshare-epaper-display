---
title: Hardware setup
description: Prepare the Pi and connect the e-Paper HAT.
layout: libdoc_page.liquid
permalink: getting-started/hardware-setup/index.html
tags:
    - getting-started
eleventyNavigation:
    key: Hardware setup
    parent: Getting Started
    order: 2
---

## Prepare the Pi

Use the [Raspberry Pi imager](https://www.raspberrypi.com/software/) and install **Raspberry Pi OS Lite**.

Ensure that you have SSH access, or direct access, to the Raspberry Pi, and that it can connect to the Internet to download packages. 

In most cases you would do this via the imager's settings screen: set the username and password, enable **SSH** and set up **WiFi** access.

## Connect the display

Turn the Pi off, then put the HAT on top of the Pi's GPIO pins.

Connect the ribbon from the epaper display to the extension. To do this you will need to lift the black latch at the back of the connector, insert the ribbon slowly, then push the latch down.

Now turn the Pi back on and SSH into it.

