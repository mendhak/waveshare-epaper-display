
. env.sh

function log {
    echo "---------------------------------------"
    echo ${1^^}
    echo "---------------------------------------"
}

if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
    export WAVESHARE_WIDTH=640
    export WAVESHARE_HEIGHT=384
else
    export WAVESHARE_WIDTH=800
    export WAVESHARE_HEIGHT=480
fi

if [ $PRIVACY_MODE = 1 ]; then
    log "Get XKCD comic strip"
    .venv/bin/python3 xkcd_get.py
    if [ $? -eq 0 ]; then
        .venv/bin/python3 display.py xkcd-comic-strip.png
    fi

else

    log "Add weather info"
    .venv/bin/python3 screen-weather-get.py

    log "Add Calendar info"
    .venv/bin/python3 screen-calendar-get.py

    # Only layout 5 shows a calendar, so save a few seconds.
    if [ "$SCREEN_LAYOUT" -eq 5 ]; then
        log "Add Calendar month"
        .venv/bin/python3 screen-calendar-month.py
    fi

    if [ -f screen-custom-get.py ]; then
        log "Add Custom data"
        .venv/bin/python3 screen-custom-get.py
    elif [ ! -f screen-output-custom-temp.svg ]; then
        # Create temporary empty svg since the main SVG needs it
        echo "<svg />" > screen-output-custom-temp.svg
    fi

    if [[ ! -z "$INKY_DISPLAY_TYPE" ]]; then
      log "Resize svg"
      . resolution.sh
      .venv/bin/python3 inky-resize.py
      export WAVESHARE_WIDTH=$INKY_DISPLAY_WIDTH
      export WAVESHARE_HEIGHT=$INKY_DISPLAY_HEIGHT
    fi

    log "Export to PNG"

    .venv/bin/cairosvg -o screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-output-weather.svg

    if [[ ! -z "$INKY_DISPLAY_TYPE" ]]; then
        .venv/bin/python3 InkyDisplay.py --type ${INKY_DISPLAY_TYPE} --colour ${INKY_DISPLAY_COLOR} -i screen-output.png
    else
        .venv/bin/python3 display.py screen-output.png
    fi
fi
