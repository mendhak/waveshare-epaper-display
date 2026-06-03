#!/usr/bin/env bash

function log {
    echo "---------------------------------------"
    echo "${1^^}"
    echo "---------------------------------------"
}

if [[ -f env.sh ]]; then
    echo "This project has switched to using config.toml. "
    echo "Run .venv/bin/python3 utils/migrate_env_to_toml.py to generate your config.toml from the existing env.sh."
    echo "Or, copy config.example.toml to config.toml and edit the values you need"
    echo "You can then edit it to make any adjustments."
    echo "Remember to remove the env.sh afterwards."
    exit 1
fi

if [[ ! -f config.toml ]]; then
    echo "No config.toml found. Copy config.example.toml to config.toml and edit."
    exit 1
fi

mkdir -p data

# Read some specific values as env vars, it's needed here
eval $(.venv/bin/python3 scripts/run_config_toml_helper.py)


if [[ $WAVESHARE_EPD75_VERSION = 1 ]]; then
    export WAVESHARE_WIDTH=640
    export WAVESHARE_HEIGHT=384
else
    export WAVESHARE_WIDTH=800
    export WAVESHARE_HEIGHT=480
fi

if [[ $PRIVACY_ENABLED = 1 ]]; then
    if [[ $PRIVACY_MODE = "xkcd" ]]; then
        log "Get XKCD comic strip"
        if .venv/bin/python3 scripts/screen_xkcd_get.py; then
            .venv/bin/python3 scripts/display.py data/xkcd-comic-strip.png
        fi
    else
        log "Get Literature Clock"
        if .venv/bin/python3 scripts/screen_literature_clock_get.py; then
            .venv/bin/cairosvg -u -o data/screen_literature_clock.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT data/screen_literature_clock.svg
            .venv/bin/python3 scripts/display.py data/screen_literature_clock.png
        fi
    fi
else
    log "Add weather info"
    if ! .venv/bin/python3 scripts/screen_weather_get.py; then
        log "⚠️Error getting weather, stopping."
        exit 1
    fi

    log "Add Calendar info"
    if ! .venv/bin/python3 scripts/screen_calendar_get.py; then
        log "⚠️Error getting calendar info, stopping."
        exit 1
    fi

    # Only layout 5 shows a calendar, so save a few seconds.
    if [[ "$SCREEN_LAYOUT" -eq 5 ]]; then
        log "Add Calendar month"
        if ! .venv/bin/python3 scripts/screen_calendar_month.py; then
            log "⚠️Error getting calendar month info, stopping."
            exit 1
        fi
    fi

    if [[ -f scripts/screen_custom_get.py ]]; then
        log "Add Custom data"
        if ! .venv/bin/python3 scripts/screen_custom_get.py; then
            log "⚠️Error getting custom data, stopping."
            exit 1
        fi
    fi

    # Create temporary empty svg if it doesn't exist or is empty
    if [[ ! -f data/screen_output_custom_temp.svg ]] || [[ ! -s data/screen_output_custom_temp.svg ]]; then
        echo -n '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"></svg>' > data/screen_output_custom_temp.svg
    fi


    log "Export to PNG"

    # .venv/bin/cairosvg -u -o screen_output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT screen_output_weather.svg
    if ! .venv/bin/cairosvg -u -o data/screen_output.png -f png --dpi 300 --output-width $WAVESHARE_WIDTH --output-height $WAVESHARE_HEIGHT data/screen_output_weather.svg; then
        log "⚠️Error exporting to PNG, stopping."
        exit 1
    fi

    log "Display on screen"

    .venv/bin/python3 scripts/display.py data/screen_output.png
fi
