"""
STEP 1
Simple plot rendering
Each plot is saved in a separate HTML file

HoloViews reference: https://holoviews.org/index.html
"""

import pandas as pd
import numpy as np
import holoviews as hv
hv.extension('bokeh')

df = pd.read_csv('../data/softdrinkco2.csv')

# Plotting a scatterplot
scatter = hv.Scatter(df).opts(width=500, height=400, size=5, tools=['hover'])
hv.save(scatter, '../output/step1_scatter.html')

# Plotting a Histogram
frequencies, edges = np.histogram(df, bins=15)
hist = hv.Histogram((edges, frequencies)).opts(width=500, height=400, tools=['hover'])

hv.save(hist, '../output/step1_hist.html')