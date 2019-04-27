Instructions on setting up a Raspberry Pi Zero WH with a Waveshare ePaper 7.5 Inch HAT. 

## Shopping list

[Waveshare 7.5 inch epaper display HAT 640x384](https://www.amazon.co.uk/gp/product/B075R4QY3L/)  
[Raspberry Pi Zero WH (presoldered header)](https://www.amazon.co.uk/gp/product/B07BHMRTTY/)  
[microSDHC card](https://www.amazon.co.uk/gp/product/B073K14CVB)

## Setup the PI

Use [Etcher](https://etcher.io) to write the SD card with the [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) image, no need for desktop.

After the image has been written,

### Enable SSH 

Create a file called `ssh` in the boot partition of the card.

    sudo touch /media/mendhak/boot/ssh

### Enable WiFi

Create a file called `wpa_supplicant.conf` in the boot partition 

    sudo nano /media/mendhak/boot/wpa_supplicant.conf

with these contents    


    update_config=1
    country=GB

    network={
        ssid="yourwifi"
        psk="wifipasswd"
        key_mgmt=WPA-PSK
    }


### Start the Pi

Connect the Pi to power, let it boot up.  In your router devices page, a new connected device should appear.  If all goes correctly then the pi should be available with its FQDN even.

    ssh pi@raspberrypi.lan

Login with the default password of raspberry and change it using `passwd`

### Connect the display

Put the HAT on top of the Pi's GPIO pins.  

Connect the ribbon from the epaper display to the extension.  To do this you will need to lift the black latch at the back of the connector, insert the ribbon slowly, then push the latch down. 


## Setup dependencies

    supo apt install git ttf-wqy-zenhei ttf-wqy-microhei python3-pip python-imaging libopenjp2-7-dev libjpeg8-dev inkscape
    sudo pip3 install spidev RPi.GPIO Pillow  # Pillow took multiple attempts to install as it's always missing dependencies
    sudo sed -i s/#dtparam=spi=on/dtparam=spi=on/ /boot/config.txt  #This enables SPI
    sudo reboot

### Get the BCM2835 driver

    wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.58.tar.gz
    sudo tar zxvf bcm2835-1.58.tar.gz
    cd bcm2835-1.58/
    sudo ./configure
    sudo make
    sudo make check
    sudo make install


### Get the WiringPi library

    sudo git clone git://git.drogon.net/wiringPi
    cd wiringPi
    sudo ./build

### Get the Python3 libraries

    sudo apt-get install 
    

## Run the script

Modify the `env.sh` file and put your DarkSky API key in there. 
    
Run `./run.sh` which should query DarkSky and create a png, then display the png on screen. 




## Waveshare documentation and sample code

Waveshare have a [user manual](https://www.waveshare.com/w/upload/7/74/7.5inch-e-paper-hat-user-manual-en.pdf) which you can get to from [their Wiki](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT)


The [Waveshare demo repo is here](https://github.com/waveshare/e-Paper).  Assuming all dependencies are installed, these demos should work.  

    git clone https://github.com/waveshare/e-Paper waveshare-epaper-sample
    cd waveshare-epaper-sample





### Run the BCM2835 demo


    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/bcm2835/
    make
    sudo ./epd


### Run the WiringPI demo

    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/wiringpi/
    make
    sudo ./epd

### Run the Python3 demo

    cd ~/waveshare-epaper-sample/7.5inch_e-paper_code/RaspberryPi/python3/
    sudo python3 main.py
