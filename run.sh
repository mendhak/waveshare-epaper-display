#!/usr/bin/env bash

. env.sh

function log {
    echo "---------------------------------------"
    echo "${1^^}"
    echo "---------------------------------------"
}

if [[ $WAVESHARE_EPD75_VERSION = 1 ]]; then
    export WAVESHARE_WIDTH=640
    export WAVESHARE_HEIGHT=384
else
    export WAVESHARE_WIDTH=800
    export WAVESHARE_HEIGHT=480
fi

if [[ $PRIVACY_MODE_XKCD = 1 ]]; then
    log "Get XKCD comic strip"
    .venv/bin/python3 xkcd_get.py
    if [ $? -eq 0 ]; then
        .venv/bin/python3 display.py xkcd-comic-strip.png
    fi
elif [[ $PRIVACY_MODE_LITERATURE_CLOCK = 1 ]]; then
    log "Get Literature Clock"
    .venv/bin/python3 screen-literature-clock-get.py
    if [[ $? -eq 0 ]]; then
        .venv/bin/cairosvg -o screen-literature-clock.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-literature-clock.svg
        .venv/bin/python3 display.py screen-literature-clock.png
    fi
else

    log "Add weather info"
    .venv/bin/python3 screen-weather-get.py

    if [[ $? -ne 0 ]]; then
        log "⚠️Error getting weather, stopping."
        exit 1
    fi

    log "Add Calendar info"
    .venv/bin/python3 screen-calendar-get.py

    if [[ $? -ne 0 ]]; then
        log "⚠️Error getting calendar info, stopping."
        exit 1
    fi

    # Only layout 5 shows a calendar, so save a few seconds.
    if [[ "$SCREEN_LAYOUT" -eq 5 ]]; then
        log "Add Calendar month"
        .venv/bin/python3 screen-calendar-month.py

        if [[ $? -ne 0 ]]; then
            log "⚠️Error getting calendar month info, stopping."
            exit 1
        fi
    fi

    if [[ -f screen-custom-get.py ]]; then
        log "Add Custom data"
        .venv/bin/python3 screen-custom-get.py

        if [[ $? -ne 0 ]]; then
            log "⚠️Error getting custom data, stopping."
            exit 1
        fi

    elif [[ ! -f screen-output-custom-temp.svg ]]; then
        # Create temporary empty svg since the main SVG needs it
        echo "<svg />" > screen-output-custom-temp.svg
    fi


    log "Export to PNG"

    .venv/bin/cairosvg -o screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-output-weather.svg

    log "Display on screen"

    .venv/bin/python3 display.py screen-output.png
fi
