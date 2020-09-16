# normal imports
import pandas as pd

# bokeh imports
from bokeh.io import show
from bokeh.io import curdoc

# module imports
import source.plots as plots


# data read
data = pd.read_csv("nowcasts/data/data.csv", parse_dates=["date_forecast", "target_period"])

p = plots.gen_plot(data, "x_vol_world2", "2020-09-01")

# final layout
curdoc().add_root(p)
curdoc().title = "UNCTAD Nowcasts"
