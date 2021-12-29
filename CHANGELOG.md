## 2021-12-29

* Updated instructions for Raspberry Pi OS Bullseye.  Many dependencies stopped working, fixed it now. 
* Removed some dependencies that aren't needed anymore! BCM not needed.  WiringPi is deprecated.  LibJpeg doesn't look needed.  
* Replace Inkscape with CairoSVG. Inkscape broke some commandline args, and CairoSVG seems better suited for commandline anyway. 
* Updated Google Calendar instructions, it's simpler for now, until Google break their URLs again. 

## 2021-10-29

* Bug fix - Outlook calendar entries will now show in local time, instead of UTC. 

## 2021-08-13

* Calendar entries will include all events from today, even if they are past.   

## 2021-08-10

* Calendar entries will now show the start and end times

## 2021-07-29

* Implemented mechanism for Severe Alert provider
* Added Met Office RSS feed as the first severe alert provider

## 2021-04-20

* Implemented mechanism for Weather provider
* Added VisualCrossing, AccuWeather, Met.No, MetOffice, OpenWeatherMap, ClimaCell weather providers

## 2021-04-03

* Switch to Met Office daily forecast instead of 3-hourly

## 2021-04-02

* Add Outlook Calendar functionality

## Before all that

* Basic weather, time and event dashboard.  
* There were a few weather providers hardcoded
* There was PiHole stats but I removed it
* There was TFL train times but I removed it
