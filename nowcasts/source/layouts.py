from bokeh.layouts import column, row, Spacer
from bokeh.models.widgets import Tabs, Panel, Div

def gen_layout(p, catalog, target_dropdown, target_period_dropdown, pred_text, commentary):
	# tabs
	plot_tab = Panel(child=row(p), title="Nowcasts")
	
	# metadata tab
	metadata_text = """
<body>
<h4>Metadata</h4>
<p>
some text
</p>
"""
	metadata = Div(text=metadata_text, width=600)
	metadata_tab = Panel(
		child=column(metadata), title="Metadata"
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
	
	tabs = Tabs(tabs=[plot_tab, metadata_tab, notes_tab])
	
	# final layout
	layout = column(
		Spacer(height=15),
		row(column(target_dropdown), column(target_period_dropdown)),
		Spacer(height=15),
		Div(text=pred_text, width=1200),
		Div(text=commentary),
		Spacer(height=15),
		row(tabs)
	)
	return layout