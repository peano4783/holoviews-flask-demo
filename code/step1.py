"""
STEP 1
Rendering two HoloViews plots; each plot is saved in a separate HTML file; pure HoloViews, no Flask yet
"""

import pandas as pd
import numpy as np
import holoviews as hv
hv.extension('bokeh')

# Reading data from file
df = pd.read_csv('../data/softdrinkco2.csv')

# Generating a HoloViews scatterplot
scatter = hv.Scatter(df).opts(width=500, height=400, size=5, tools=['hover'])
# Saving the scatterplot in an HTML file
hv.save(scatter, '../output/step1_scatter.html')

# Generating a HoloViews histogram
frequencies, edges = np.histogram(df, bins=15)
hist = hv.Histogram((edges, frequencies)).opts(width=500, height=400, tools=['hover'])

# Saving the histogram in an HTML file
hv.save(hist, '../output/step1_hist.html')