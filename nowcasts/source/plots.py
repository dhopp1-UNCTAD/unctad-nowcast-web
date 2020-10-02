# normal imports
import datetime as dt
import pandas as pd

# bokeh imports
from bokeh.plotting import figure
from bokeh.models import Legend, HoverTool

def gen_plot(data, target, target_name, target_period, palette):
	# title sizing
	title_text_font_size = "14pt"
	axis_text_font_size = "11pt"
	axis_label_font_size = "14pt"
	
	# for the forecast line
	mask = (data.series == "forecast") & (data.target == target) & (data.target_period == target_period)
	line_data = data.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	line_data["date_forecast_string"] = line_data.date_forecast.apply(lambda x: str(x)[:10])
	
	# for the stacked bars
	stack = data.loc[
		(data.target == target) & 
		(data.target_period == target_period) & 
		(data.series != "forecast")
		, ["date_forecast", "series", "value"]]
	stack = stack.pivot(index="date_forecast", columns="series", values="value").reset_index()
	stack = stack.fillna(0)
	
	# plot
	p = figure(
			title=f"{target_name}: {target_period[:4]} Q{int(int(target_period[5:7])/3)} nowcast quarter-over-quarter growth",
			x_axis_type="datetime", 
			x_axis_label="Date nowcast made",
			y_axis_label="Percent",
			plot_width=1200, 
			plot_height=600
	)
	p.add_layout(Legend(), 'right')
	p.vbar_stack(
			stackers=stack.columns[1:], 
			x="date_forecast", 
			source=stack, 
			legend_label=list(stack.columns[1:]), 
			color=palette[:len(stack.columns[1:])], 
			width=dt.timedelta(days=5),
			name="stack"
	)
	p.line("date_forecast", "value", source=line_data, line_width=1.5, color="black", name="forecast")
	p.title.text_font_size = title_text_font_size # title
	p.xaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.yaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.xaxis.axis_label_text_font_size = axis_label_font_size # axis label
	p.yaxis.axis_label_text_font_size = axis_label_font_size # axis label
	
	# tool tips
	# for stacked bar chart
	tooltips = list(zip(
			pd.Series(stack.columns[1:]), 
			pd.Series(stack.columns[1:])
			.apply(lambda x: "@{" + x + "}{0.00}%"))
	)
	
	p.add_tools(
        HoverTool(
            tooltips=[
                ("Date", "@date_forecast_string"),
                ("Target period nowcast", "@value{0.00}%")
            ],
            names=["forecast"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=tooltips,
            names=["stack"],
            mode="mouse"
        )
	)
		
	# text for display
	pred_text = f"""
<p><strong>Date of latest nowcast made:</strong> {str(line_data.date_forecast.values[-1])[:10]}</p>
<p><strong>Latest nowcast:</strong> {round(line_data.value.values[-1], 2)}%</p>
	"""
	
	return [p, pred_text]
