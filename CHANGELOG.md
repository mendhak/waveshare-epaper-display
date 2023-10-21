## 2023-10-21
* Point at OpenWeatherAPI version 3. Added by [jcolladosp](https://github.com/mendhak/waveshare-epaper-display/pull/71)

## 2023-10-15
* Updated instructions for Raspberry Pi OS October 2023 edition, which comes with Python 3.11 and breaks a few dependencies. 

## 2023-03-10
* Ability to set the timezone name for Google Calendar, with the `GOOGLE_CALENDAR_TIME_ZONE_NAME` variable. This is necessary if you're using Google's Family Calendar feature, which is hardcoded to UTC. 

## 2023-02-13
* Breaking change - the setup now runs under a Python virtual environment for safety and easy recovery. If you are updating, rerun the README instructions. 
* Localization - the time format and date format will now be formatted according to the Raspberry Pi's default locale. Usually this is `en_GB` but can be changed using `raspi-config`.  
* The font used to display the text will also be based on the Raspberry Pi's locale. Whatever `fc-match sans-serif` says is the font that gets used. The default for most Western locales is DejaVu Sans. 
* It's possible to pick another locale by setting the `LANG` environment variable in the env.sh, instructions added for that. 
* It's possible to override the font, I've added instructions for that.  But it's really basic. I don't know much about font config. 


## 2023-02-04
* Add SMHI (Sweden) as weather provider. Added by [hnnweb](https://github.com/mendhak/waveshare-epaper-display/pull/51)

## 2023-01-29
* Add code to display on the [7.5 inch B version 2 screen](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat-b.htm)

## 2023-01-21
* Downgrade 'cryptography' as its package was yanked in [the wheels](https://www.piwheels.org/project/cryptography/).  By [@jokeum](https://github.com/mendhak/waveshare-epaper-display/pull/48)
* Bugfix: can't compare offset-naive and offset-aware datetimes by [@jokeum](https://github.com/mendhak/waveshare-epaper-display/pull/49). 

## 2022-11-30
* ICS and CalDav calendar support added by [anthonyscorrea](https://github.com/mendhak/waveshare-epaper-display/pull/43)
* Moved pip package list into requirements.txt.  The package versions are fixed, it's simpler to install, and better stability.
* Refactored the calendar code into providers and simplified the code for better reuse
* Added instructions and VSCode integration for running and debugging the project locally

## 2022-10-04
* Bugfix: an `&` ampersand in event title would cause image generation to crash.

## 2022-04-21
* By default, past calendar events will disappear from the list.
* Added option to show all past events from today, `CALENDAR_INCLUDE_PAST_EVENTS_FOR_TODAY=1`

## 2022-04-13
* Add new layouts for the user to choose from. Set the value `export SCREEN_LAYOUT=1` to 2, 3, 4...
* Layouts contributed by @feh123 and @jmason
* Added the ability to have custom SVGs added onto the rendered output.  Done via `screen-custom-get.py` and `screen-custom.svg`.
* Bugfix: Multi day events will now show start and end days. eg, "Monday - Wednesday"

## 2022-04-10
* Use friendly day names for calendar entries, like "Today", "Tonight", "Tomorrow".
* If the calendar entry is within the next 6 days use the day name "Monday" "Tuesday", else use "Mon Apr 18".

## 2022-04-08
* Add Met Éireann weather and alert provider by [@jmason](https://github.com/mendhak/waveshare-epaper-display/pull/34)

## 2022-03-06
* Add weather.gov as a weather and alert provider
* Add VisualCrossing instructions to the README
* Rename the weather and alert and calendar cache files to use a `cache_` prefix.  A little consistency.

## 2022-01-07

* Add cryptography==36.0.0 to setup. It's used by msal, but version 36.0.1 from piwheels produces [illegal instruction](https://github.com/piwheels/packages/issues/273)
* Add gsfonts to setup.  It contains Nimbus fonts required by the SVG.

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
