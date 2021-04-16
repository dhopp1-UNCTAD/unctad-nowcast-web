from bokeh.layouts import column, row, Spacer
from bokeh.models.widgets import Tabs, Panel, Div, DataTable, TableColumn
from bokeh.plotting import ColumnDataSource

def gen_layout(p, comp, gdp_plot, catalog, model_dropdown, target_dropdown, target_period_dropdown, target_period_gdp_dropdown, pred_text, commentary):
	# tabs
	plot_tab = Panel(child=row(p), title="News Plot")
	comparison_tab = Panel(child=row(comp), title="Comparison Plot")
	gdp_tab = Panel(child=column(
		row(target_period_gdp_dropdown),
		row(gdp_plot)
	), title="GDP News Plot")
	
	# metadata tab
	cat = catalog.loc[(catalog.x_world > 0) | (catalog.x_vol_world2 > 0) | (catalog.x_servs_world > 0),:].reset_index(drop=True)
	# adding column for which model in
	def which_in(one, two, three):
		outstr = ""
		if one:
			outstr += "Total merchandise exports"
		if two:
			outstr += " | Exports of services, world"
		if three:
			outstr += " | Export volumes, world (UNCTAD)"
		if outstr[0] == " ":
			outstr = outstr[2:]
		return outstr
		
	catalog["nowcasts"] = cat.apply(lambda x: which_in(x["x_world"], x["x_servs_world"], x["x_vol_world2"]), axis=1)
	cat = catalog.loc[:,["Variable", "Frequency", "Units", "Source", "nowcasts"]].sort_values(by=["Variable"])
	metadata_source = ColumnDataSource(dict(cat))
	columns = [
	    TableColumn(
	        field="Variable",
	        title="Variable"),
	    TableColumn(
	        field="Frequency",
	        title="Frequency"),
		TableColumn(
	        field="Units",
	        title="Units"),
		TableColumn(
	        field="Source",
	        title="Source"),
		TableColumn(
	        field="nowcasts",
	        title="Nowcasts in"),
    ]
	data_table = DataTable(
	    source=metadata_source, columns=columns, width=1200, height=1200, row_height=25, autosize_mode="fit_columns"
	)
	
	metadata_tab = Panel(
		child=data_table, title="Metadata"
	)
	
	# methodology tab
	notes_text = """
<body>
<h4>Definition and methodology</h4>
<p>
UNCTAD’s global merchandise trade nowcasts are real-time estimates of current trends in international trade in goods based on timely information from many data sources. The nowcasts presented correspond to total merchandise trade in value and volumes for the previous and current quarters. The preceding period is included to fill the publication gap: while the preceding quarter has elapsed, official figures will only be available after several months. Timely information is obtained from numerous official statistics and other country- and regional-level indicators of trade, industrial production, domestic trade, freight transportation, trade prices, and business and consumer surveys. UNCTAD updates its nowcast estimates once per week, reflecting new information releases and data revisions. All figures represent quarter-overquarter growth rates of seasonally adjusted series. For more details on the methodology and underlying indicators, see <a href="https://unctad.org/en/pages/PublicationWebflyer.aspx?publicationid=2301">this</a> working paper and <a href="https://unctad.org/meetings/en/Presentation/20200203%20Nowcast%20workshop_UNCTAD2.pdf">this</a> presentation.
</p>
	"""
	notes = Div(text=notes_text, width=600)
	notes_tab = Panel(
	    child=column(notes), title="Methodology"
	)
	
	tabs = Tabs(tabs=[plot_tab, comparison_tab, metadata_tab, notes_tab, gdp_tab])
	
	# final layout
	layout = column(
		Div(text=commentary),
		Spacer(height=15),
		row(column(model_dropdown)),
		Spacer(height=15),
		row(column(target_dropdown), column(target_period_dropdown)),
		Spacer(height=15),
		Div(text=pred_text, width=1200),
		Spacer(height=15),
		row(tabs)
	)
	return layout