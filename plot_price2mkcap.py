from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import export_svgs, export_png
import json

PRICE_FILE = "price-indices/prices.json"
ISSUE_FILE = "price-indices/securities.json"
OUTPUT_FILE = "www/price2mkcap.html"


marketcaps = []   # registered shares x latest price
price_changes = []
symbols = []

with open(PRICE_FILE,"r") as f:
    price_data = json.loads(f.read())['data']

with open(ISSUE_FILE,"r") as f:
    issue_data = json.loads(f.read())['data']

# make plot
for symbol in issue_data.keys():
    if symbol in price_data:
        print symbol, issue_data[symbol]['name_th']

        try:
            p = price_data[symbol]['price_latest']
            p = float(p)
            c = price_data[symbol]['pct_change']
            c = float(c)

            shares_count = issue_data[symbol]['registered_shares']
            market_cap = shares_count * p / 1000000.0
        except Exception as e:
            print symbol, str(e)

        marketcaps.append(market_cap)
        price_changes.append(c)
        s_label = "{0} [{1} {2}% {3}]".format(symbol,market_cap,c,p)
        symbols.append(s_label)

data = {'x_values': marketcaps,
        'y_values': price_changes,
        'symbols': symbols}

source = ColumnDataSource(data=data)

print marketcaps

# output to static HTML file
title = "Changes to Market Cap (15 minute delay, source: SetTrade.com)"
p = figure(title=title, plot_width=1400, plot_height=700, x_range=(0,500000), x_axis_type="log",  y_range=(-15,30))

# add a circle renderer with a size, color, and alpha
p.circle(x='x_values', y='y_values', source=source, size=5, color="navy", alpha=0.5)


labels = LabelSet(x='x_values', y='y_values', text='symbols', level='glyph',
              x_offset=-15, y_offset=5, source=source, text_font_size="8pt", render_mode='canvas')
p.add_layout(labels)

p.add_layout(Title(text="Market Cap (Million-THB)", align="center"), "below")
p.add_layout(Title(text="Price Change (%)", align="center"), "left")


# show the results
# show(p)

# Create output
hout = file_html(p, CDN, "ThaiMarketCap.com - Change vs Market Cap")

with open(OUTPUT_FILE, "w") as f:
    f.write(hout)
