---
title: Font
description: Replace the default font used on the display.
layout: libdoc_page.liquid
permalink: appearance/font/index.html
tags:
    - appearance
eleventyNavigation:
    key: Font
    parent: Appearance
    order: 2
---

The default font is set to `sans-serif` which on a Raspberry Pi defaults to DejaVu Sans. It's a decent font, wide, and visible, and works for most western languages.

In this example I'll replace it with Noto Sans. You can do this with whichever font you prefer.  

First run this command to show the current font being used.

```bash
$ fc-match sans-serif
DejaVuSans.ttf: "DejaVu Sans" "Book"
```

Install Noto fonts.

```bash
sudo apt install fonts-noto
```

Now create a font config file if it doesn't already exist.

```bash
mkdir -p ~/.config/fontconfig/conf.d
nano ~/.config/fontconfig/conf.d/00-fonts.conf
```

Set the contents of the `00-fonts.conf` file:

```xml
<?xml version='1.0'?>
<!DOCTYPE fontconfig SYSTEM 'fonts.dtd'>
<fontconfig>
  <alias>
    <family>sans-serif</family>
    <prefer>
        <family>Noto Sans</family>
    </prefer>
  </alias>
</fontconfig>
```

This tells the system to prefer 'Noto Sans' if the 'sans-serif' family is requested. You can test it by running:

```bash
$ fc-match sans-serif
NotoSans-Regular.ttf: "Noto Sans" "Regular"
```

The next time `run.sh` runs, the output image should have the chosen font.
