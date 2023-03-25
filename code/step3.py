"""
STEP 3
Making an interactive plot

The code uses the file /templates/step3_index.html
"""

from flask import Flask, request, render_template, abort, Response, redirect
import pandas as pd
import numpy as np
from bokeh.embed import components
import holoviews as hv
import bokeh
hv.extension('bokeh')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    dataset_name = 'softdrinkco2'

    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')

    df = pd.read_csv('../data/' + dataset_name + '.csv')

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

    return render_template('step3_index.html',
                           title='My flask application',
                           bokeh_version=bokeh.__version__,
                           dataset_name = dataset_name,
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)