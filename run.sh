. env.sh
sudo -E python3 weather-get.py


# Inkscape can't export to BMP, so let's export to PNG first. 
inkscape  screen-output-weather.svg --without-gui -e screen-output.png -w640 -h384 --export-dpi=150

# Convert to a black and white, 1 bit bitmap
convert -colors 2 +dither -type Bilevel -monochrome screen-output.png screen-output.bmp

sudo display/display screen-output.bmp
