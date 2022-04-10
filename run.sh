
. env.sh

function log {
    echo "---------------------------------------"
    echo ${1^^}
    echo "---------------------------------------"
}

log "Get Weather info"
python3 screen-weather-get.py

log "Get Calendar info"
python3 screen-calendar-get.py

log "Get Custom data"
python3 screen-custom-get.py

log "Export to PNG"

if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
    WAVESHARE_WIDTH=640
    WAVESHARE_HEIGHT=384
else
    WAVESHARE_WIDTH=800
    WAVESHARE_HEIGHT=480
fi

cairosvg -o screen-output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen-output-weather.svg

log "Display on epaper"
python3 display.py screen-output.png
