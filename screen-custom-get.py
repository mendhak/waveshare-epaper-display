import logging
from utility import update_svg, configure_logging

configure_logging()

def main():
    output_svg_filename = 'screen-custom.svg'

    # Your custom code here like getting PiHole Status, car charger status, API calls. 
    # Edit the screen-custom.svg to change position, font size, add more custom data. 
    custom_value_1 = "";

    logging.info("Updating SVG")
    output_dict = {
        'CUSTOM_DATA_1' : custom_value_1
    }
    update_svg('screen-custom.svg', 'screen-output-custom-temp.svg', output_dict)

if __name__ == "__main__":
    main()
