#! /bin/bash

[[ -z ""${LINE}"" ]] && LINE=`.venv/bin/python3 InkyDisplay.py --type ${INKY_DISPLAY_TYPE} --colour ${INKY_DISPLAY_COLOR} -r`

if [[ $LINE =~([[:digit:]]+),[[:space:]]([[:digit:]]+) ]]; then
    export INKY_DISPLAY_WIDTH=${BASH_REMATCH[1]}
    export INKY_DISPLAY_HEIGHT=${BASH_REMATCH[2]}
    echo "INKY_DISPLAY_WIDTH=${INKY_DISPLAY_WIDTH}"
    echo "INKY_DISPLAY_HEIGHT=${INKY_DISPLAY_HEIGHT}"
fi
