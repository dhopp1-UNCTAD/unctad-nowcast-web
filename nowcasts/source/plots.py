# normal imports
import datetime as dt

# bokeh imports
from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.models import Legend

def gen_plot(data, target, target_period):
	# for the forecast line
	mask = (data.target == target) & (data.target_period == target_period) & (data.series == "forecast")
	x = data.loc[mask, "date_forecast"].reset_index(drop=True)
	y = data.loc[mask, "value"].reset_index(drop=True)
	
	# for the stacked bars
	stack = data.loc[
		(data.target == target) & 
		(data.target_period == target_period) &
		(data.series != "forecast")
		, ["date_forecast", "series", "value"]]
	stack = stack.pivot(index="date_forecast", columns="series", values="value").reset_index()
	stack = stack.fillna(0)
	
	# plot
	p = figure(x_axis_type='datetime', plot_width=1600, plot_height=800)
	p.add_layout(Legend(), 'right')
	p.vbar_stack(
			stackers=stack.columns[1:], 
			x="date_forecast", 
			source=stack, 
			legend_label=list(stack.columns[1:]), 
			color=Category20[len(stack.columns[1:])], 
			width=dt.timedelta(days=5)
	)
	p.line(x, y, line_width=1.5, color="black")
	
	return p
