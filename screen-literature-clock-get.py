import random
import codecs
import textwrap
from utility import is_stale
import requests
import csv
import datetime
import re


if is_stale('litclock_annotated.csv', 86400):
    url = "https://raw.githubusercontent.com/JohannesNE/literature-clock/master/litclock_annotated.csv"
    response = requests.get(url)
    response.raise_for_status()
    with open('litclock_annotated.csv', 'w') as text_file:
        text_file.write(response.text)

time_rows = []
current_time = datetime.datetime.now().strftime("%H:%M")
print(current_time)
#current_time = "13:48"
with open('litclock_annotated.csv', 'r') as file:
    reader = csv.DictReader(file,
                            fieldnames=[
                                "time", "time_human", "full_quote", "book_title", "author_name", "sfw"],
                            delimiter='|',
                            lineterminator='\n',
                            quotechar=None, quoting=csv.QUOTE_NONE)
    for row in reader:
        if row["time"] == current_time and row["sfw"] != "nsfw":
            time_rows.append(row)


if len(time_rows) == 0:
    print("No quotes found for this time.")
    exit()
else:
    random_item = random.choice(time_rows)
    quote = random_item["full_quote"]
    book = random_item["book_title"]
    author = random_item["author_name"]
    human_time = random_item["time_human"]


quote = quote.encode('ascii', 'ignore').decode('utf-8')
print(quote)

quote_length = len(quote)
if quote_length < 105:
    font_size = 55
    max_chars_per_line = 25
elif quote_length < 205:
    font_size = 45
    max_chars_per_line = 30
elif quote_length < 305:
    font_size = 35
    max_chars_per_line = 35
elif quote_length < 405:
    font_size = 30
    max_chars_per_line = 45
else:
    font_size = 25
    max_chars_per_line = 55


attribution = f"- {book}, {author}"
author_font_subtraction = 5
if len(attribution) > max_chars_per_line:
    attribution = attribution[:max_chars_per_line] + "…"
    author_font_subtraction = 12


print(f"Quote length: {quote_length}, Font size: {font_size}, Max chars per line: {max_chars_per_line}, Subtraction: {author_font_subtraction}")

quote = quote.replace("<br/>", " ")
quote = quote.replace("<br />", " ")
quote = quote.replace("<br>", " ")

quote_pattern = re.compile(re.escape(human_time), re.IGNORECASE)
# Replace human time by itself but surrounded by pipes for later processing.
quote = quote_pattern.sub(lambda x: f"|{x.group()}|", quote)

lines = textwrap.wrap(quote, width=max_chars_per_line, break_long_words=True)

generated_quote = ""
time_ends_on_next_line = False
for line in lines:
    start_span = ""
    end_span = ""

    if line.count("|") == 2:
        line = line.replace("|", "<tspan style='font-weight:bold;'>", 1)
        line = line.replace("|", "</tspan>", 1)

    if line.count("|") == 1 and not time_ends_on_next_line:
        line = line.replace("|", "<tspan style='font-weight:bold;'>", 1)
        time_ends_on_next_line = True
        end_span = "</tspan>"

    if line.count("|") == 1 and time_ends_on_next_line:
        line = line.replace("|", "</tspan>", 1)
        time_ends_on_next_line = False
        start_span = "<tspan style='font-weight:bold;'>"

    generated_quote += f"""
        <tspan x="33" dy="1.2em">{start_span}{line}{end_span}</tspan>
    """

generated_quote += f"""
        <tspan x="150" dy="1.5em" style="font-size:{font_size-author_font_subtraction}px;">{attribution}</tspan>
"""

svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg height="480" width="800" version="1.1">
        <rect width="800" height="480" id="rect3855" fill="white" />

        <text id="quote" x="33" y="15" style="font-size:{font_size}px;line-height:0%;font-family:serif;text-anchor:beginning">

                {generated_quote}
        </text>
</svg>

"""

output_svg_filename = 'screen-literature-clock.svg'

svg_output = svg_template

codecs.open(output_svg_filename, 'w', encoding='utf-8').write(svg_output)
