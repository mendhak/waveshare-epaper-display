import tomllib
import json

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

print(json.dumps(config, indent=4))

print(config["display"]["waveshare_version"])
print(config["display"]["screen_output_layout"])
print(config["privacy"]["xkcd"])
print(config["privacy"]["literature_clock"])
