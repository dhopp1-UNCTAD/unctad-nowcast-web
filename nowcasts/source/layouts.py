from bokeh.layouts import column, row, Spacer
from bokeh.models.widgets import Tabs, Panel, Div, TableColumn, DataTable
from bokeh.plotting import ColumnDataSource

def gen_layout(p, catalog, target_dropdown, target_period_dropdown):
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
	
	# table for variable explanation
	columns = [
	    TableColumn(
	        title="Variable abbreviation",
	        field="code",
	        width=175,
	    ),
		TableColumn(
	        title="Variable description",
	        field="name",
	        width=175,
	    ),
		TableColumn(
	        title="Source",
	        field="source",
	        width=175,
	    )
	]
	catalog = catalog.sort_values("code")
	cat_dict = {'code':list(catalog.code), 'name':list(catalog.name), 'source':list(catalog.source)}
	source_cat = ColumnDataSource(cat_dict)
	cat_table = DataTable(
	    source=source_cat,
	    columns=columns,
	    width=1200,
	    height=600,
	    fit_columns=False,
	    index_width=0,
	    row_height=25,
	)
	cat_tab = Panel(child=row(cat_table), title="Variable explanation")
	
	tabs = Tabs(tabs=[plot_tab, cat_tab, notes_tab])
	
	# final layout
	layout = column(
		Spacer(height=15),
		row(column(target_dropdown), column(target_period_dropdown)),
		Spacer(height=15),
		row(tabs)
	)
	return layout