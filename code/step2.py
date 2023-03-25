"""
STEP 2
Creating a simple web app and display two plots at a time

The code uses the file /templates/step2_index.html

Watch carefully for bokeh_version: it must match the one that is in your system.
Use "pip show bokeh" to determine the version of Bokeh in your system.


This is where I got my inspiration on how to put together Bokeh and Flask:
https://www.gcptutorials.com/post/creating-charts-with-bokeh-and-flask
"""

from flask import Flask, request, render_template, abort, Response, redirect
import pandas as pd
import numpy as np
from bokeh.embed import components
import holoviews as hv
hv.extension('bokeh')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    df = pd.read_csv('../data/softdrinkco2.csv')

    # Isolate the first column to be our dataset:
    data = df.iloc[:, 0]

    # Plotting a scatterplot
    scatter = hv.Scatter(data).opts(width=500, height=400, tools=['hover'])

    # Plotting a Histogram
    frequencies, edges = np.histogram(data, bins=15)
    hist = hv.Histogram((edges, frequencies)).opts(width=500, height=400, tools=['hover'])

    bokeh_scatter = hv.render(scatter)
    scatter_script, scatter_div = components(bokeh_scatter)

    bokeh_hist = hv.render(hist)
    hist_script, hist_div = components(bokeh_hist)

    return render_template('step2_index.html',
                           title='My flask application',
                           bokeh_version='2.4.3',
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)