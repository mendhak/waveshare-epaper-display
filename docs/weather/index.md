---
title: Choose a weather provider
description: Pick one of the weather providers for temperature and forecasts.
layout: libdoc_page.liquid
permalink: weather/index.html
tags:
    - weather
eleventyNavigation:
    key: Weather
    order: 3
---
{% alert 'You can only use one weather provider at a time. <br /> But, you can configure several and switch between them if needed.', 'info', 'Choosing a provider' %}

You can pick between the following to provide temperature and weather forecasts.

* [OpenWeatherMap](openweathermap.md)
* [Met Office](met-office.md)
* [AccuWeather](accuweather.md)
* [Met.no](met-no.md)
* [Weather.gov](weathergov.md)
* [VisualCrossing](visualcrossing.md)
* [Climacell](climacell.md)
* [Met Éireann](met-eireann.md)
* [SMHI](smhi.md) 

In each case, you will choose a provider under the `[weather]` section which you created in the [Location step](/configuration/location.md), and then add another section for the specific provider.

Each provider is configured differently, please follow the instructions carefully for each provider.
