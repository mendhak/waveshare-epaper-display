---
title: Choosing a weather provider
description: Pick one of the supported weather providers for temperature and forecasts.
layout: libdoc_page.liquid
permalink: weather/index.html
tags:
    - weather
eleventyNavigation:
    key: Weather
    order: 3
---
{% alert 'You can only use one weather provider at a time.', 'info', 'Choosing a provider' %}

You can pick between OpenWeatherMap, Met Office, AccuWeather, Met.no, Weather.gov, VisualCrossing, Climacell, Met Éireann, SMHI to provide temperature and weather forecasts.

In `config.toml`, under the same `[weather]` section, set the `provider` to the provider you want to use. For example:

```toml
[weather]
... your location details from above ...
provider = "metoffice"                # metoffice, climacell, accuweather, openweathermap, metno, met_eireann, weathergov, smhi, visualcrossing
```

Then configure the API key (or self-identification) in the corresponding provider section linked below:

* [OpenWeatherMap](/weather/openweathermap/)
* [Met Office (UK)](/weather/met-office/)
* [AccuWeather](/weather/accuweather/)
* [Met.no](/weather/met-no/)
* [Met Éireann (Ireland)](/weather/met-eireann/)
* [Weather.gov (US)](/weather/weathergov/)
* [Climacell (tomorrow.io)](/weather/climacell/)
* [VisualCrossing](/weather/visualcrossing/)
* [SMHI (Sweden)](/weather/smhi/)
