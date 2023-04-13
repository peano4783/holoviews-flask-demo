"""
STEP 4
A full-scale web app for performing process capability analysis
"""

from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import bokeh
import holoviews as hv
hv.extension('bokeh')

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index_page():
    # Setting default parameters
    dataset_name = 'softdrinkco2.csv'
    lsl, usl = "", ""
    connect_dots = ""
    pointsize = 4
    show_Cp = ""
    show_Cpk = ""
    show_Cpm = ""
    show_hist = "checked"
    nbins = 15
    show_distr = ""

    # Reading default parameters from the web form when the user clicks on Submit
    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')
        lsl = request.form.get('lsl')
        usl = request.form.get('usl')
        pointsize = int(request.form.get('pointsize'))
        connect_dots = "checked" if "connect_dots" in request.form else ""
        show_Cp = "checked" if "show_Cp" in request.form else ""
        show_Cpk = "checked" if "show_Cpk" in request.form else ""
        show_Cpm = "checked" if "show_Cpm" in request.form else ""
        show_hist = "checked" if "show_hist" in request.form else ""
        nbins = int(request.form.get('nbins'))
        show_distr = "checked" if "show_distr" in request.form else ""

    # If LSL or USL values are non-numerical, we interpret them as non-existent
    try:
        lsl = float(lsl)
    except:
        lsl = ""
    try:
        usl = float(usl)
    except:
        usl = ""

    df = pd.read_csv('../data/' + dataset_name)

    # Setting the visibility limits given lsl, usl and the dataset
    range_diff = (usl if usl else df.iloc[:, 0].max()) - (lsl if lsl else df.iloc[:, 0].min())
    lims = (lsl - range_diff*0.1 if lsl and (lsl<df.iloc[:, 0].min()) else None,
            usl + range_diff*0.1 if usl and (usl>df.iloc[:, 0].max()) else None)

    # Plotting a scatterplot
    scatter = hv.Scatter(df).opts(width=600, height=300, ylim=lims, xlabel="Time", ylabel="Reading", size=pointsize, tools=['hover'])
    # Connecting scatterplot dots if necessary
    if connect_dots:
        scatter = scatter * hv.Curve(df)

    # Plotting LSL/USL horizontal bars
    if lsl:
        scatter = hv.HLine(lsl).opts(line_width=1, color="red") * scatter
    if usl:
        scatter = hv.HLine(usl).opts(line_width=1, color="red") * scatter

    # Evaluating Cp, Cpk and Cpm values:
    Cps, Cpks, Cpms = [], [], []
    if show_Cp or show_Cpk or show_Cpm:
        for i in range(len(df.iloc[:, 0])):
            m = df.iloc[:i+1, 0].mean()
            s = df.iloc[:i+1, 0].std()
            if lsl and usl:
                Cps.append((usl-lsl)/(6*s))
                Cpks.append(min((m - lsl)/(3 * s), (usl - m)/(3 * s)))
                T = (lsl + usl) / 2
                Cpms.append(Cps[-1]/np.sqrt(1+((m-T)/s)**2))
            elif lsl:
                Cps.append((m - lsl)/(3 * s))
                Cpks.append(Cps[-1])
            elif usl:
                Cps.append((usl - m)/(3 * s))
                Cpks.append(Cps[-1])
        C_plot = None
        if Cps and show_Cp:
            Cp_series = pd.DataFrame({'Cp': Cps})
            Cp_plot = hv.Scatter(Cp_series, label='Cp').opts(width=600, height=300, size=pointsize, tools=['hover'])
            if connect_dots:
                Cp_plot = Cp_plot * hv.Curve(Cp_series)
            C_plot = C_plot * Cp_plot if C_plot else Cp_plot
        if Cpks and show_Cpk:
            Cpk_series = pd.DataFrame({'Cpk': Cpks})
            Cpk_plot = hv.Scatter(Cpk_series, label='Cpk').opts(width=600, height=300, size=pointsize, tools=['hover'])
            if connect_dots:
                Cpk_plot = Cpk_plot * hv.Curve(Cpk_series)
            C_plot = C_plot * Cpk_plot if C_plot else Cpk_plot
        if Cpms and show_Cpm:
            Cpm_series = pd.DataFrame({'Cpm': Cpms})
            Cpm_plot = hv.Scatter(Cpm_series, label='Cpm').opts(width=600, height=300, size=pointsize, tools=['hover'])
            if connect_dots:
                Cpm_plot = Cpm_plot * hv.Curve(Cpm_series)
            C_plot = C_plot * Cpm_plot if C_plot else Cpm_plot
        if C_plot:
            scatter = hv.Layout(scatter + C_plot).cols(1)

    # Plotting a Histogram
    frequencies, edges = np.histogram(df, bins=nbins)
    h, d = None, None
    if show_hist:
        h = hv.Histogram((edges, frequencies)).opts(width=600, height=300, xlim=lims, tools=['hover'])
    if show_distr:
        d = hv.Distribution(df).opts(width=600, height=300, xlim=lims, tools=['hover'])
    if lsl:
        vlin = hv.VLine(lsl).opts(line_width=1, color="red")
        if h:
            h = h * vlin
        if d:
            d = d * vlin
    if usl:
        vlin = hv.VLine(usl).opts(line_width=1, color="red")
        if h:
            h = h * vlin
        if d:
            d = d * vlin
    if h and d:
        hist = hv.Layout(h + d).cols(1)
    elif h:
        hist = h
    elif d:
        hist = d
    else:
        hist = None

    bokeh_scatter = hv.render(scatter)
    scatter_script, scatter_div = bokeh.embed.components(bokeh_scatter)

    # If no hist is due to be displayed, we leave the placeholders for both JavaScript and HTML empty.
    hist_script, hist_div = "", ""
    if hist:
        bokeh_hist = hv.render(hist)
        hist_script, hist_div = bokeh.embed.components(bokeh_hist)

    return render_template('step4_index.html',
                           title='Process Capability Indices (Six Sigma)',
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
                           scatter_script = scatter_script,
                           scatter_div = scatter_div,
                           hist_script = hist_script,
                           hist_div = hist_div)

if __name__ == '__main__':
    app.run(debug=True)