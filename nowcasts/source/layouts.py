from bokeh.layouts import column, row, Spacer
from bokeh.models.widgets import Tabs, Panel, Div

def gen_layout(p, catalog, target_dropdown, target_period_dropdown, pred_text):
	# tabs
	plot_tab = Panel(child=row(p), title="Nowcasts")
	notes_text = """
<h4>Placeholder text</h4>
<p>
Information on methodology.
<br>
	"""
	notes = Div(text=notes_text, width=600)
	notes_tab = Panel(
	    child=column(notes), title="Methodology"
	)
	tabs = Tabs(tabs=[plot_tab, notes_tab])
	
	# final layout
	layout = column(
		Spacer(height=15),
		row(column(target_dropdown), column(target_period_dropdown)),
		Spacer(height=15),
		Div(text=pred_text, width=1200),
		Spacer(height=15),
		row(tabs)
	)
	return layout