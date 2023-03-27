"""
STEP 2
Creating a simple web app and display two plots on the same page

The code uses the file /templates/step2_index.html

This is where I got my inspiration on how to put together Bokeh and Flask:
https://www.gcptutorials.com/post/creating-charts-with-bokeh-and-flask
"""
from flask import Flask, request, render_template, abort, Response, redirect
import pandas as pd
import numpy as np
import bokeh
import holoviews as hv
hv.extension('bokeh')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    df = pd.read_csv('../data/softdrinkco2.csv')

    # Plotting a scatterplot
    scatter = hv.Scatter(df).opts(width=500, height=300, size=5, tools=['hover'])

    # Plotting a Histogram
    frequencies, edges = np.histogram(df, bins=15)
    hist = hv.Histogram((edges, frequencies)).opts(width=500, height=300, tools=['hover'])

    bokeh_scatter = hv.render(scatter)
    scatter_script, scatter_div = bokeh.embed.components(bokeh_scatter)

    bokeh_hist = hv.render(hist)
    hist_script, hist_div = bokeh.embed.components(bokeh_hist)

    return render_template('step2_index.html',
                           title='My Flask application',
                           bokeh_version=bokeh.__version__,
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)