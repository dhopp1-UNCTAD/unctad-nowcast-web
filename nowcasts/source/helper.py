def convert_quarter(entry, quarter_to_date):
	# from Q3 to -09-01
	if quarter_to_date:
		conversion = f"{entry[:4]}-{str(int(entry[-1:]) * 3).zfill(2)}-01"
	else:
		conversion = f"{entry[:4]} Q{int(int(entry[5:7])/3)}"
	return conversion

def get_full_var_name(catalog, var_name, var_to_name):
	if var_to_name:
		return_name = catalog.loc[catalog.code == var_name, "name"].values[0]
	else:
		return_name = catalog.loc[catalog.name == var_name, "code"].values[0]
	return return_name