
. env.sh

function log {
    echo "---------------------------------------"
    echo ${1^^}
    echo "---------------------------------------"
}

log "Get Weather info"
sudo -E python3 screen-weather-get.py

current_hour=`date +"%H"`


log "Get Calendar info"
sudo -E python3 screen-calendar-get.py

log "Export to PNG"

if [ $WAVESHARE_EPD75_VERSION = 1 ]; then
    WAVESHARE_WIDTH=640
    WAVESHARE_HEIGHT=384
else
    WAVESHARE_WIDTH=800
    WAVESHARE_HEIGHT=480
fi

inkscape screen-output-weather.svg --without-gui -e screen-output.png -w$WAVESHARE_WIDTH -h$WAVESHARE_HEIGHT --export-dpi=300

# Convert to a black and white, 1 bit bitmap
#convert -colors 2 +dither -type Bilevel -monochrome screen-output.png screen-output.bmp


SHOULD_REFRESH=0
current_minute=`date +"%M"`

log "Display on epaper"
sudo python3 display.py screen-output.png
