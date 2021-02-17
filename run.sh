
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

log "Export to PNG"

if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
    WAVESHARE_WIDTH=640
    WAVESHARE_HEIGHT=384
else
    WAVESHARE_WIDTH=800
    WAVESHARE_HEIGHT=480
fi

inkscape screen-output-weather.svg --without-gui -e screen-output.png -w$WAVESHARE_WIDTH -h$WAVESHARE_HEIGHT --export-dpi=300

log "Display on epaper"
python3 display.py screen-output.png
