
. env.sh

function log {
    echo "---------------------------------------"
    echo ${1^^}
    echo "---------------------------------------"
}

if [ $PRIVACY_MODE = 1 ]; then
    log "Display on epaper"
    .venv/bin/python3 display.py xkcd-comic-strip.png

else

    log "Add weather info"
    .venv/bin/python3 screen-weather-get.py

    log "Add Calendar info"
    .venv/bin/python3 screen-calendar-get.py

    if [ -f screen-custom-get.py ]; then
        log "Add Custom data"
        .venv/bin/python3 screen-custom-get.py
    elif [ ! -f screen-output-custom-temp.svg ]; then
        # Create temporary empty svg since the main SVG needs it
        echo "<svg />" > screen-output-custom-temp.svg
    fi


    log "Export to PNG"

    if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
        WAVESHARE_WIDTH=640
        WAVESHARE_HEIGHT=384
    else
        WAVESHARE_WIDTH=800
        WAVESHARE_HEIGHT=480
    fi

    .venv/bin/cairosvg -o screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-output-weather.svg


    .venv/bin/python3 display.py screen-output.png
fi