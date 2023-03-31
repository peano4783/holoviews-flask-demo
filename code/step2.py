"""
STEP 2
Creating a simple web app and displaying two plots on the same page
"""

from flask import Flask, render_template
import pandas as pd
import numpy as np
import bokeh
import holoviews as hv
hv.extension('bokeh')

# Defining a Flask app
app = Flask(__name__)

# Function that returns the HTML contents of the Flask app's main page
@app.route('/', methods=['GET', 'POST'])
def index_page():
    # Reading data from file
    df = pd.read_csv('../data/softdrinkco2.csv')

    # Generating a HoloViews scatterplot
    scatter = hv.Scatter(df).opts(width=500, height=300, size=5, tools=['hover'])

    # Generating a HoloViews histogram
    frequencies, edges = np.histogram(df, bins=15)
    hist = hv.Histogram((edges, frequencies)).opts(width=500, height=300, tools=['hover'])

    # Distilling the HoloViews objects scatter and hist into Bokeh objects and
    bokeh_scatter, bokeh_hist = hv.render(scatter), hv.render(hist)

    # generating JavaScript and HTML for the Bokeh objects
    scatter_script, scatter_div = bokeh.embed.components(bokeh_scatter)
    hist_script, hist_div = bokeh.embed.components(bokeh_hist)

    # Using step2_index.html template to generate an actual HTML page.
    # JavaScript and HTML of the graphs are passed to the template among other parameters.
    return render_template('step2_index.html',
                           title='My Flask application',
                           bokeh_version=bokeh.__version__,
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)