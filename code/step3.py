"""
STEP 3
Creating a web app with a plot and adding interactivity

The code uses the file /templates/step3_index.html
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
    dataset_name = 'softdrinkco2.csv'
    pointsize = 4
    nbins = 15

    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')
        pointsize = int(request.form.get('pointsize'))
        nbins = int(request.form.get('nbins'))

    df = pd.read_csv('../data/' + dataset_name)

    # Plotting a scatterplot
    scatter = hv.Scatter(df).opts(width=600, height=300, size=pointsize, tools=['hover'])

    # Plotting a Histogram
    frequencies, edges = np.histogram(df, bins=nbins)
    hist = hv.Histogram((edges, frequencies)).opts(width=600, height=300, tools=['hover'])

    bokeh_scatter = hv.render(scatter)
    scatter_script, scatter_div = bokeh.embed.components(bokeh_scatter)

    bokeh_hist = hv.render(hist)
    hist_script, hist_div = bokeh.embed.components(bokeh_hist)

    return render_template('step3_index.html',
                           title='My Flask application',
                           bokeh_version=bokeh.__version__,
                           dataset_name = dataset_name,
                           pointsize = pointsize,
                           nbins = nbins,
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)