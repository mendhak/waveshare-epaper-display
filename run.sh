#!/bin/bash

(
set -x
. env.sh

function log {
    echo "---------------------------------------"
    echo ${1^^}
    echo "---------------------------------------"
}

# crash out if any of these fail

log "Get Weather info"
timeout $TIMEOUT python3 screen-weather-get.py || \
    timeout $TIMEOUT python3 screen-weather-get.py || \
    timeout $TIMEOUT python3 screen-weather-get.py || exit 1

log "Get HomeAssistant info"
timeout $TIMEOUT python3 screen-homeassistant-get.py || \
    timeout $TIMEOUT python3 screen-homeassistant-get.py || \
    timeout $TIMEOUT python3 screen-homeassistant-get.py || exit 1

log "Get Calendar info"
timeout $TIMEOUT python3 screen-calendar-get.py || \
    timeout $TIMEOUT python3 screen-calendar-get.py || \
    timeout $TIMEOUT python3 screen-calendar-get.py || exit 1

log "Export to PNG"

if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
    WAVESHARE_WIDTH=640
    WAVESHARE_HEIGHT=384
else
    WAVESHARE_WIDTH=800
    WAVESHARE_HEIGHT=480
fi

# inkscape screen-output-calendar.svg --without-gui -e screen-output.png -w$WAVESHARE_WIDTH -h$WAVESHARE_HEIGHT --export-dpi=300
cairosvg -o screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-output-calendar.svg

log "Separate black/red channels"
convert screen-output.png -channel R -separate only_black.png
pngtopnm screen-output.png > screen-output.pnm
pngtopnm only_black.png > only_black.pnm
ppmtopgm only_black.pnm | pnmsmooth | pgmtopbm -threshold -value 0.9999 | pbmmask > mask.pbm
pnminvert mask.pbm > mask_invert.pbm
pnmcomp -alpha=mask_invert.pbm mask_invert.pbm screen-output.pnm only_red.pnm
pnmtopng only_red.pnm > only_red.png

# Convert to a black and white, 1 bit bitmap
convert -colors 2 +dither -type Bilevel -monochrome only_red.png only_red.bmp
convert -colors 2 +dither -type Bilevel -monochrome only_black.png only_black.bmp

log "Display on epaper"
python3 display.py only_black.bmp only_red.bmp

) 2>&1 | tee -a run.log
