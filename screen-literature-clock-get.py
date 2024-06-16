import codecs
import textwrap


quote = """
It was nine-twenty one. With one minute to go, there was no sign of Herbert’s mother.
"""

# quote="""Must have the phone disconnected. Some contractor keeps calling me up about payment for 50 bags of cement he claims I collected ten days ago. Says he helped me load them onto a truck himself. I did drive Whitby's pick-up into town but only to get some lead screening. What does he think I'd do with all that cement? Just the sort of irritating thing you don't expect to hang over your final exit. (Moral: don't try too hard to forget Eniwetok.) Woke 9:40. To sleep 4:15."""
# book = "This is life"
# author = "Dan Rhodes"

# quote="""
#     At the hour of 9:46 A.M., to be exact, as one should in these matters, I had cast three times above the known lair of this fish. Then I cast a fourth time, more from habit than hope; and the fight was on.
# """
book = "Ma Pettengill"
author = "Harry Leon Wilson"

quote = """
At only nine in the morning, the kitchen was already pregnant to its capacity, every crevice and countertop overtaken by Marjan’s gourmet creations. Marinating vegetables (𝘵𝘰𝘳𝘴𝘩𝘪𝘴 of mango, eggplant, and the regular seven-spice variety), packed to the briny brims of five-gallon see-through canisters sat on the kitchen island. Large blue bowls were filled with salads (angelica lentil, tomato, cucumber and mint, and Persian fried chicken), 𝘥𝘰𝘭𝘮𝘦𝘩, and dips (cheese and walnut, yogurt and cucumber, baba ghanoush, and spicy hummus), which along with feta, Stilton, and cheddar cheeses, were covered and stacked in the enormous glass-door refrigerator.
"""
# book = "Pomegranate Soup"
# author = "Marsha Mehran"

book = "Narrative of a Journey Round the Dead Sea and in the Bible Lands in 1850 and 1851"
author = "Tom Clancy, Steve Pieczenik, and Jeff Rovin"

quote = quote.encode('ascii', 'ignore').decode('utf-8')

quote_length = len(quote)
if quote_length < 100:
    font_size = 45
    max_chars_per_line = 28
elif quote_length < 308:
    font_size = 35
    max_chars_per_line = 45
else:
    font_size = 25
    max_chars_per_line = 55

if len(book) > 20:
    book = book[:20] + "…"
    font_size_subtraction = 12
if len(author) > 20:
    author = author[:20] + "…"
    font_size_subtraction = 12


lines = textwrap.wrap(quote, width=max_chars_per_line, break_long_words=True)

generated_quote = ""
for line in lines:
    generated_quote += f"""
        <tspan x="33" dy="1.2em">{line}</tspan>
    """

generated_quote += f"""
        <tspan x="150" dy="1.5em" style="font-size:{font_size-font_size_subtraction}px;">- {book}, <tspan style="font-style:italic;">{author}</tspan></tspan>
"""

svg_template = f"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg height="480" width="800" version="1.1">
        <rect width="800" height="480" id="rect3855" fill="white" />

        <text id="quote" x="33" y="15" style="font-size:{font_size}px;line-height:0%;font-family:Bookerly,serif;text-anchor:beginning">

                {generated_quote}
        </text>
</svg>

"""

output_svg_filename = 'screen-literature-clock.svg'

svg_output = svg_template

codecs.open(output_svg_filename, 'w', encoding='utf-8').write(svg_output)
