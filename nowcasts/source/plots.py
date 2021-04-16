# normal imports
import datetime as dt
import pandas as pd
import numpy as np

# bokeh imports
from bokeh.plotting import figure
from bokeh.models import Legend, HoverTool, CustomJS

def gen_plot(data, actuals, target, target_name, target_period, palette):
	# title sizing
	title_text_font_size = "14pt"
	axis_text_font_size = "11pt"
	axis_label_font_size = "14pt"
	
	# for the forecast line
	mask = (data.series == "forecast") & (data.target == target) & (data.target_period == target_period)
	line_data = data.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	line_data["date_forecast_string"] = line_data.date_forecast.apply(lambda x: str(x)[:10])
	
	# for the actuals line
	actual_data = actuals.loc[actuals.date == target_period,target].values[0] * 100
	actual_line = line_data.loc[:,["date_forecast"]]
	actual_line["actual"] = actual_data
    
	# for the stacked bars
	stack = data.loc[
		(data.target == target) & 
		(data.target_period == target_period) & 
		(data.series != "forecast")
		, ["date_forecast", "series", "value"]]
	stack = stack.pivot(index="date_forecast", columns="series", values="value").reset_index()
	stack = stack.fillna(0)
	
	pos_stack = stack.copy()
	for col in stack.columns[1:]:
		pos_stack.loc[pos_stack[col] < 0,col] = 0
	neg_stack = stack.copy()
	for col in stack.columns[1:]:
		neg_stack.loc[neg_stack[col] >= 0,col] = 0
	
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
	# positive values
	p.vbar_stack(
			stackers=pos_stack.columns[1:], 
			x="date_forecast", 
			source=pos_stack, 
			legend_label=list(pos_stack.columns[1:]), 
			color=palette[:len(pos_stack.columns[1:])], 
			width=dt.timedelta(days=5),
			name="pos_stack"
	)
	# negative values
	p.vbar_stack(
			stackers=neg_stack.columns[1:], 
			x="date_forecast", 
			source=neg_stack, 
			legend_label=list(neg_stack.columns[1:]), 
			color=palette[:len(neg_stack.columns[1:])], 
			width=dt.timedelta(days=5),
			name="neg_stack"
	)
	p.line("date_forecast", "value", source=line_data, line_width=1.5, color="black", name="forecast")
	p.line("date_forecast", "actual", source=actual_line, line_width=1.5, color="black", line_dash="dotted", name="actual")
	p.title.text_font_size = title_text_font_size # title
	p.xaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.yaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.xaxis.axis_label_text_font_size = axis_label_font_size # axis label
	p.yaxis.axis_label_text_font_size = axis_label_font_size # axis label
	
	# tool tips
	# for stacked bar chart
	pos_tooltips = list(zip(
			pd.Series(stack.columns[1:]) + " (+ contribution)", 
			pd.Series(stack.columns[1:])
			.apply(lambda x: "@{" + x + "}{0.00}%"))
	)
	neg_tooltips = list(zip(
			pd.Series(stack.columns[1:]) + " (- contribution)", 
			pd.Series(stack.columns[1:])
			.apply(lambda x: "@{" + x + "}{0.00}%"))
	)
	
	p.add_tools(
        HoverTool(
            tooltips=[
                ("Date of nowcast", "@date_forecast_string"),
                ("DFM nowcast", "@value{0.00}%")
            ],
            names=["forecast"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=[
                ("Target period", target_period),
                ("Actual value", "@actual{0.00}%")
            ],
            names=["actual"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=pos_tooltips,
            names=["pos_stack"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=neg_tooltips,
            names=["neg_stack"],
            mode="mouse"
        )
	)
		
	# text for display
	pred_text = f"""
<p><strong>Date of latest nowcast made:</strong> {str(line_data.date_forecast.values[-1])[:10]}</p>
<p><strong>Latest nowcast:</strong> {round(line_data.value.values[-1], 2)}%</p>
	"""
	
	return [p, pred_text]


def gen_comparison_plot(dfm, lstm, actuals, target, target_name, target_period, palette):
	# title sizing
	title_text_font_size = "14pt"
	axis_text_font_size = "11pt"
	axis_label_font_size = "14pt"
	
	# for the dfm line
	mask = (dfm.series == "forecast") & (dfm.target == target) & (dfm.target_period == target_period)
	dfm_data = dfm.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	dfm_data["date_forecast_string"] = dfm_data.date_forecast.apply(lambda x: str(x)[:10])

	# for the lstm line
	mask = (lstm.series == "forecast") & (lstm.target == target) & (lstm.target_period == target_period) & (lstm.date_forecast <= np.max(dfm_data.date_forecast)) & (lstm.date_forecast >= np.min(dfm_data.date_forecast))
	lstm_data = lstm.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	lstm_data["date_forecast_string"] = lstm_data.date_forecast.apply(lambda x: str(x)[:10])
	
	# for the actuals line
	actual_data = actuals.loc[actuals.date == target_period,target].values[0] * 100
	actual_line = dfm_data.loc[:,["date_forecast"]]
	actual_line["actual"] = actual_data

	# for 0 line
	mask = (lstm.series == "forecast") & (lstm.target == target) & (lstm.target_period == target_period) & (lstm.date_forecast <= np.max(dfm_data.date_forecast)) & (lstm.date_forecast >= np.min(dfm_data.date_forecast))
	zero_data = lstm.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	zero_data.value = 0
	zero_data["date_forecast_string"] = zero_data.date_forecast.apply(lambda x: str(x)[:10])
    	
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
	p.line("date_forecast", "value", source=dfm_data, line_width=1.5, color="blue", name="DFM", legend_label="DFM")
	p.line("date_forecast", "value", source=lstm_data, line_width=1.5, color="red", name="LSTM", legend_label="LSTM")
	p.line("date_forecast", "actual", source=actual_line, line_width=1.5, color="black", line_dash="dotted", name="actual", legend_label = "Actual value")
	p.line("date_forecast", "value", source=zero_data, line_width=1.5, color="black", name="zero")
	
	p.title.text_font_size = title_text_font_size # title
	p.xaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.yaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.xaxis.axis_label_text_font_size = axis_label_font_size # axis label
	p.yaxis.axis_label_text_font_size = axis_label_font_size # axis label
	
	# tool tips
	# for stacked bar chart
	p.add_tools(
        HoverTool(
            tooltips=[
                ("Date of nowcast", "@date_forecast_string"),
                ("DFM nowcast", "@value{0.00}%")
            ],
            names=["DFM"],
            mode="mouse"
        ),
        HoverTool(
            tooltips=[
                ("Date of nowcast", "@date_forecast_string"),
                ("LSTM nowcast", "@value{0.00}%")
            ],
            names=["LSTM"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=[
                ("Target period", target_period),
                ("Actual value", "@actual{0.00}%")
            ],
            names=["actual"],
            mode="mouse"
        )
	)
	
	return p


def gen_gdp_plot(gdp, actuals, target_period, palette):
	# title sizing
	title_text_font_size = "14pt"
	axis_text_font_size = "11pt"
	axis_label_font_size = "14pt"
	
	target_period = str(target_period) + "-12-01"

	# for the forecast line
	mask = (gdp.series == "forecast") & (gdp.target_period == target_period)
	line_data = gdp.loc[mask, ["date_forecast", "value"]].reset_index(drop=True)
	line_data["date_forecast_string"] = line_data.date_forecast.apply(lambda x: str(x)[:10])
	
	# for the actuals line
	# does this date exist in the actuals
	if pd.to_datetime(target_period) <= np.max(pd.to_datetime(actuals.date)):
		actual_data = actuals.loc[actuals.date == target_period,"gdp_world"].values[0] * 100
	else:
		actual_data = np.nan
	actual_line = line_data.loc[:,["date_forecast"]]
	actual_line["actual"] = actual_data


	# for the stacked bars
	stack = gdp.loc[
		(gdp.target == "gdp_world") & 
		(gdp.target_period == target_period) & 
		(gdp.series != "forecast")
		, ["date_forecast", "series", "value"]]
	stack = stack.pivot(index="date_forecast", columns="series", values="value").reset_index()
	stack = stack.fillna(0)
	
	pos_stack = stack.copy()
	for col in stack.columns[1:]:
		pos_stack.loc[pos_stack[col] < 0,col] = 0
	neg_stack = stack.copy()
	for col in stack.columns[1:]:
		neg_stack.loc[neg_stack[col] >= 0,col] = 0
	
	# plot
	p = figure(
			title=f"GDP: {target_period[:4]} nowcast year-over-year growth",
			x_axis_type="datetime", 
			x_axis_label="Date nowcast made",
			y_axis_label="Percent",
			plot_width=1200, 
			plot_height=600
	)
	p.add_layout(Legend(), 'right')
	# positive values
	p.vbar_stack(
			stackers=pos_stack.columns[1:], 
			x="date_forecast", 
			source=pos_stack, 
			legend_label=list(pos_stack.columns[1:]), 
			color=palette[:len(pos_stack.columns[1:])], 
			width=dt.timedelta(days=5),
			name="pos_stack"
	)
	# negative values
	p.vbar_stack(
			stackers=neg_stack.columns[1:], 
			x="date_forecast", 
			source=neg_stack, 
			legend_label=list(neg_stack.columns[1:]), 
			color=palette[:len(neg_stack.columns[1:])], 
			width=dt.timedelta(days=5),
			name="neg_stack"
	)
	p.line("date_forecast", "value", source=line_data, line_width=1.5, color="black", name="forecast")
	p.line("date_forecast", "actual", source=actual_line, line_width=1.5, color="black", line_dash="dotted", name="actual")
	p.title.text_font_size = title_text_font_size # title
	p.xaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.yaxis.major_label_text_font_size = axis_text_font_size # axis ticks
	p.xaxis.axis_label_text_font_size = axis_label_font_size # axis label
	p.yaxis.axis_label_text_font_size = axis_label_font_size # axis label
	
	# tool tips
	# for stacked bar chart
	pos_tooltips = list(zip(
			pd.Series(stack.columns[1:]) + " (+ contribution)", 
			pd.Series(stack.columns[1:])
			.apply(lambda x: "@{" + x + "}{0.00}%"))
	)
	neg_tooltips = list(zip(
			pd.Series(stack.columns[1:]) + " (- contribution)", 
			pd.Series(stack.columns[1:])
			.apply(lambda x: "@{" + x + "}{0.00}%"))
	)
	
	p.add_tools(
        HoverTool(
            tooltips=[
                ("Date of nowcast", "@date_forecast_string"),
                ("LSTM nowcast", "@value{0.00}%")
            ],
            names=["forecast"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=[
                ("Target period", target_period),
                ("Actual value", "@actual{0.00}%")
            ],
            names=["actual"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=pos_tooltips,
            names=["pos_stack"],
            mode="mouse"
        ),
		HoverTool(
            tooltips=neg_tooltips,
            names=["neg_stack"],
            mode="mouse"
        )
	)

	return p
