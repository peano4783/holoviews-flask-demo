"""
STEP 4
Building an advanced interactive plot

The code uses the file /templates/step4_index.html
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
    lsl, usl = '(None)', '(None)'
    connect_dots = ""
    pointsize = 4
    show_Cp = ""
    show_Cpk = ""
    show_Cpm = ""
    show_hist = "checked"
    nbins = 15
    show_distr = "checked"
    hist_distr_same_graph = "checked"

    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')
        pointsize = int(request.form.get('pointsize'))
        connect_dots = "checked" if "connect_dots" in request.form else ""
        show_Cp = "checked" if "show_Cp" in request.form else ""
        show_Cpk = "checked" if "show_Cpk" in request.form else ""
        show_Cpm = "checked" if "show_Cpm" in request.form else ""
        show_hist = "checked" if "show_hist" in request.form else ""
        nbins = int(request.form.get('nbins'))
        show_distr = "checked" if "show_distr" in request.form else ""
        hist_distr_same_graph = "checked" if "hist_distr_same_graph" in request.form else ""

    df = pd.read_csv('../data/' + dataset_name )

    # Plotting a scatterplot
    scatter = hv.Scatter(df).opts(width=600, height=300, size=pointsize, tools=['hover'])

    if connect_dots:
        scatter = scatter * hv.Curve(df)

    # Plotting a Histogram
    frequencies, edges = np.histogram(df, bins=nbins)
    hist = hv.Histogram((edges, frequencies)).opts(width=600, height=300, tools=['hover'])

    bokeh_scatter = hv.render(scatter)
    scatter_script, scatter_div = bokeh.embed.components(bokeh_scatter)

    bokeh_hist = hv.render(hist)
    hist_script, hist_div = bokeh.embed.components(bokeh_hist)

    return render_template('step4_index.html',
                           title='My Flask application',
                           bokeh_version=bokeh.__version__,
                           dataset_name = dataset_name,
                           lsl = lsl,
                           usl = usl,
                           pointsize = pointsize,
                           connect_dots = connect_dots,
                           show_Cp = show_Cp,
                           show_Cpk = show_Cpk,
                           show_Cpm = show_Cpm,
                           show_hist = show_hist,
                           nbins = nbins,
                           show_distr = show_distr,
                           hist_distr_same_graph = hist_distr_same_graph,
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)