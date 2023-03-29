"""
STEP 3
Creating a web app with a plot and adding interactivity
"""

from flask import Flask, render_template, request
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
    # Defining default parameters of the user interface elements
    dataset_name, pointsize, nbins = 'softdrinkco2.csv', 4, 15

    # This if clause is evoked when the user clicks on the Submit button.
    # We grab the user parameters value from the webpage form.
    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')
        pointsize = int(request.form.get('pointsize'))
        nbins = int(request.form.get('nbins'))

    # Reading data from file
    df = pd.read_csv('../data/' + dataset_name)

    # Generating a HoloViews scatterplot
    scatter = hv.Scatter(df).opts(width=600, height=300, size=pointsize, tools=['hover'])

    # Generating a HoloViews histogram
    frequencies, edges = np.histogram(df, bins=nbins)
    hist = hv.Histogram((edges, frequencies)).opts(width=600, height=300, tools=['hover'])

    # Distilling the HoloViews objects scatter and hist into Bokeh objects and
    # generating JavaScript and HTML for the Bokeh objects
    scatter_script, scatter_div = bokeh.embed.components(hv.render(scatter))
    hist_script, hist_div = bokeh.embed.components(hv.render(hist))

    # Using step3_index.html template to generate an actual HTML page.
    # JavaScript and HTML of the graphs are passed to the template among other parameters.
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

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)