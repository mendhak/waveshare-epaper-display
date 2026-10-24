---
title: AccuWeather
description: Configure the AccuWeather weather provider.
layout: libdoc_page.liquid
permalink: weather/accuweather/index.html
tags:
    - weather
eleventyNavigation:
    key: AccuWeather
    parent: Weather
    order: 4
---

Register on the [AccuWeather](https://developer.accuweather.com/) site.  
Next, [register a new application](https://developer.accuweather.com/user/me/apps). I just named it Personal, marked it as Limited Trial, Internal App, Business to Consumer. Once you do this you'll get an **API Key**, save it.  

You'll also need an AccuWeather **Location Key**.  
Do a normal [AccuWeather search](https://www.accuweather.com/) for your location. The last number in the URL is the Location Key. In the example of [London](https://www.accuweather.com/en/gb/london/ec4a-2/weather-forecast/328328), it's `328328`.

In `config.toml`, choose to use the AccuWeather provider by adding it under the `[weather]` section:

```toml
[weather]
... your location details from the location step ...
provider = "accuweather"
```

Then add a section for the AccuWeather provider with your API key and location key.


```toml
[weather.providers.accuweather]
api_key = "xxxxxx"
location_key = "328328"
```
