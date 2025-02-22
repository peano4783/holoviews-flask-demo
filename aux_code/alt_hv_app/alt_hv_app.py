from flask import Flask
import pandas as pd
import bokeh
import holoviews as hv
hv.extension('bokeh')

app = Flask(__name__)

@app.route('/')
def index_page():
    df = pd.DataFrame({'День': [1, 2, 3, 4, 5, 6, 7, 8],
        'Цена акции Группы Астра, руб.': [561.3, 563.5, 564.2, 575.75, 611.0, 596.4, 650.2, 713.0]})
    script, div = bokeh.embed.components(hv.render(hv.Curve(df).opts(width=500, height=400)))

    return f"""<html><body><script>const output = "Hello, world!";</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bokeh/{bokeh.__version__}/bokeh.min.js"></script>
{script} {div}</body></html>"""

if __name__ == '__main__':
    app.run(debug=True, port=8889)