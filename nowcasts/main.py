# normal imports
import pandas as pd

# bokeh imports
from bokeh.io import curdoc
from bokeh.models import Select

# module imports
import source.plots as plots
import source.palette as palette
import source.layouts as layouts
import source.helper as helper

# commentary
commentary = """
<p>
<em><strong style="font-size:20px">17 November 2020</strong></em>
<br><br>
<strong>Q3 2020</strong>
<ul>
	<li><strong><em>Total merchandise exports</em></strong>: No significant change to the forecast, strong recovery still expected.</li>
	<li><strong><em>Export volumes, world (UNCTAD)</em></strong>: No significant change to the forecast, strong recovery still expected.</li>
	<li><strong><em>Exports of services, world</em></strong>: No significant change to the forecast, services recovery still seems to be the weakest in the third quarter.</li>
</ul>
<strong>Q4 2020</strong>
<ul>
	<li><strong><em>Total merchandise exports</em></strong>: Negative news from the Russian industrial production index, Dutch merchandise exports, and HK airfreight revise the nowcast downwards. Further falls expected as the impact of the autumn COVID surge become felt.</li>
	<li><strong><em>Export volumes, world (UNCTAD)</em></strong>: Net neutral news leaves the nowcast largely unchanged, still projects as the weakest Q4 recovery of the three series.</li>
	<li><strong><em>Exports of services, world</em></strong>: The forecast continues to trend downards, this time driven by the EU industrial production index.</li>
</ul>
</p>
"""

# data read
data = pd.read_csv("nowcasts/data/data.csv", parse_dates=["date_forecast", "target_period"])
catalog = pd.read_csv("nowcasts/data/catalog.csv")
catalog = catalog.loc[catalog.code.isin(data.series.unique()),].reset_index(drop=True) # only keep variables in the nowcasts
target_options = list(pd.Series(data.target.unique()).apply(lambda x: helper.get_full_var_name(catalog, x, True)))
target_options.sort()
target_period_options = list(pd.Series(data.target_period.unique()).apply(lambda x: helper.convert_quarter(str(x), False)))
target_period_options.sort()
data.series = data.series.apply(lambda x: helper.convert_variable_code(x, catalog)) # convert variables from code to name

actuals = pd.read_csv("nowcasts/data/actuals.csv")

# initialization
target =target_options[0]
target_period = helper.convert_quarter(target_period_options[-1], quarter_to_date=True)
p, pred_text = plots.gen_plot(data, actuals, helper.get_full_var_name(catalog, target, False), target, target_period, palette.max_palette)
target_init = target_options[0]
target_period_init = target_period_options[-1]

# dropdowns
def update_plot_target(attr, old, new):
	global p, layout, target, target_dropdown, target_period_dropdown
	target = new
	p, pred_text = plots.gen_plot(data, actuals, helper.get_full_var_name(catalog, new, False), new, target_period, palette.max_palette)
	curdoc().remove_root(layout)
	layout = layouts.gen_layout(p, catalog, target_dropdown, target_period_dropdown, pred_text, commentary)
	curdoc().add_root(layout)

target_dropdown = Select(
	title="Target variable",
	options=target_options,
	value=target_init
)
target_dropdown.on_change("value", update_plot_target)
	
def update_plot_target_period(attr, old, new):
	global p, layout, target_period, target_dropdown, target_period_dropdown
	target_period = helper.convert_quarter(new, quarter_to_date=True)
	p, pred_text = plots.gen_plot(data, actuals, helper.get_full_var_name(catalog, target, False), target, helper.convert_quarter(new, quarter_to_date=True), palette.max_palette)
	curdoc().remove_root(layout)
	layout = layouts.gen_layout(p, catalog, target_dropdown, target_period_dropdown, pred_text, commentary)
	curdoc().add_root(layout)
	
target_period_dropdown = Select(
	title="Target period",
	options=target_period_options,
	value=target_period_init
)
target_period_dropdown.on_change("value", update_plot_target_period)
	
# final layout
layout = layouts.gen_layout(p, catalog, target_dropdown, target_period_dropdown, pred_text, commentary)
curdoc().add_root(layout)
curdoc().title = "UNCTAD Nowcasts"
