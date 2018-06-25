from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import export_svgs, export_png
import json

DATA_FILE = "price-indices/securities.json"
OUTPUT_FILE = "www/dividend_price.html"

dividends = []
price_to_earnings = []
symbols = []

with open(DATA_FILE,"r") as f:
    dat = json.loads(f.read())
    # print dat['data'].keys()

    s1 = dat['data'].keys()[1]
    print dat['data'][s1]['dividend_pct']

    # assemble plot data
    for s in dat['data'].keys():
        if 'dividend_pct' in dat['data'][s] and 'price_to_earning' in dat['data'][s]:
            c = dat['data'][s]['dividend_pct']
            try:
                c = float(c)
                tv = dat['data'][s]['price_to_earning']
                dividends.append(c)
                price_to_earnings.append(tv)
                # p = dat['data'][s]['price_latest']
                s_data = """{} [{} {}%]""".format(s,tv,c)
                symbols.append(s_data)
            except Exception as e:
                print s, str(e)

data = {'x_values': price_to_earnings,
        'y_values': dividends,
        'symbols': symbols}

source = ColumnDataSource(data=data)

print dividends

# output to static HTML file

title = "Dividend to P/E (Last closing, source: SetTrade.com)"
p = figure(title=title, plot_width=1400, plot_height=700, x_range=(-5,75), y_range=(-5,30))

# add a circle renderer with a size, color, and alpha
p.circle(x='x_values', y='y_values', source=source, size=5, color="navy", alpha=0.5)


labels = LabelSet(x='x_values', y='y_values', text='symbols', level='glyph',
              x_offset=-15, y_offset=5, source=source, text_font_size="8pt", render_mode='canvas')
p.add_layout(labels)


p.add_layout(Title(text="P/E (at last closing)", align="center"), "below")
p.add_layout(Title(text="Percent dividend yield (%)", align="center"), "left")


# show the results
# show(p)

# Create output
hout = file_html(p, CDN, "ThaiMarketCap.com - Dividend to P/E") 

with open(OUTPUT_FILE, "w") as f:
    f.write(hout)
