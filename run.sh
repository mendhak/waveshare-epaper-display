. env.sh
sudo -E python3 weather-get.py
exit 1

unset DISPLAY
DISPLAY=''
inkscape  screen-output-weather.svg --without-gui -e screen-output.png -w640 -h384 --export-dpi=150

sudo python3 screen-display.py

# convert -resize 640x384\!  weather-script-output.svg weather-script-output.png

# pngcrush  -q -c 0 weather-script-output.png weather-script-output_s.png

#sudo python3 weather-show.py