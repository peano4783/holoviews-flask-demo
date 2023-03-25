# HoloViews + Flask mini-tutorial
HoloViews data visualisation in a Flask web app

## Set-up
Use the `requirements.txt` file to set up the working environment:
```commandline
pip install -r requirements.txt
```

Alternatively, install the following packages in your environment manually:
```commandline
pip install holoviews
pip install flask
```

## Running
The Python files are in `code` subdirectory. 

### Datasets
- `/data/scagliarini-simulated.csv`: Table 13 of Scagliarini (2018)< 
- `/data/softdrinkco2.csv`: Table 15 of Scagliarini (2018); LSL = 5.5, USL = 8.5 
- `/data/salazar.csv`: Data from
[here](https://towardsdatascience.com/process-capability-analysis-with-r-1a4ccc2d4270).
LSL = 740, USL = 760