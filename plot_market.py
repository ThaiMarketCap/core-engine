from bokeh.plotting import figure, output_file, show
from bokeh.models import Title
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.io import export_svgs, export_png
import json

DATA_FILE = "price-indices/prices.json"
OUTPUT_FILE = "www/index.html"

price_changes = []
trade_values = []
symbols = []

with open(DATA_FILE,"r") as f:
    dat = json.loads(f.read())
    # print dat['data'].keys()

    s1 = dat['data'].keys()[1]
    print dat['data'][s1]['price_change']
    print dat['data'][s1]['shares_value_thb']

    # assemble plot data
    for s in dat['data'].keys():
        c = dat['data'][s]['price_change']
        try:
            c = float(c)
            tv = dat['data'][s]['shares_value_thb']
            price_changes.append(c)
            trade_values.append(tv)
            p = dat['data'][s]['price_latest']
            s_data = """{} [{} {}%]""".format(s,p,c)
            symbols.append(s_data)
        except Exception as e:
            print s, str(e)

data = {'x_values': trade_values,
        'y_values': price_changes,
        'symbols': symbols}

source = ColumnDataSource(data=data)

print price_changes

# output to static HTML file
output_file("current-price.html")

title = "Market @%s (15 minutes delay, source: SetTrade.com)" % dat['ts']
p = figure(title=title, plot_width=1400, plot_height=700, x_axis_type="log", y_range=(-20,20))

# add a circle renderer with a size, color, and alpha
# p.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
p.circle(x='x_values', y='y_values', source=source, size=10, color="navy", alpha=0.5)


labels = LabelSet(x='x_values', y='y_values', text='symbols', level='glyph',
              x_offset=-15, y_offset=5, source=source, text_font_size="8pt", render_mode='canvas')
p.add_layout(labels)


p.add_layout(Title(text="Value of shares traded (THB)", align="center"), "below")
p.add_layout(Title(text="Percent change of price (%)", align="center"), "left")


# show the results
# show(p)

# Create output
hout = file_html(p, CDN, "ThaiMarketCap.com") 

with open(OUTPUT_FILE, "w") as f:
    f.write(hout)
