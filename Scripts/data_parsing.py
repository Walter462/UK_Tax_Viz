
try:
    from IMPORT import pd
    from IMPORT import np
    from IMPORT import dumps
    from IMPORT import openpyxl
    from IPython.display import display, HTML
except ImportError:
    pass

#OPENPYXL
# Load the Excel file
file_path = "./attachments/Tax_calculator.xlsx"
wb = openpyxl.load_workbook(file_path, data_only=False)

# Display the contents of each sheet
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")
    for row in sheet.iter_rows(values_only=False):
        row_values = [cell.value for cell in row]
        print(row_values)
    print()
    
#PANDAS
##excel-> DataFrame
df=pd.read_excel("./attachments/Tax_calculator.xlsx")
print(df)

#Parsing pandas df-_>to arrays
##threshold names and values
thresholds_names_array = df.loc[9:12,'Unnamed: 0'].values
THRESHOLDS_VALUES = df.loc[9:12,'Unnamed: 1'].values.astype(float)
##tax rates values
dividends_tax_rates = df.loc[9:12,'Unnamed: 3'].values.astype(float)
assets_sales_tax_rates = df.loc[9:12,'Unnamed: 7'].values.astype(float)

#Hardcoding parsed arrays
thresholds_names_array = ['Personal allowance',
       'Basic rate taxpayer threshold', 'Higher rate threshold',
       'Additional rate threshold']
THRESHOLDS_VALUES = np.float64([12570, 37700, 125140, np.nan])
dividends_tax_rates = np.float64([ 0, 0.0875, 0.3375, 0.3935])
assets_sales_tax_rates = np.float64([ 0, 0.10, 0.20, 0.20])

#DICTIONARIES AND PANDAS DF
##Thresholds and their const values dictionary
threshold_and_values_dict = dict(zip(thresholds_names_array, THRESHOLDS_VALUES))
#print
#print(dumps(threshold_and_values_dict,indent=2, ensure_ascii=False))
#df
threshold_and_values_df = pd.DataFrame(data = list(threshold_and_values_dict.values()), 
             index=list(threshold_and_values_dict.keys()),
             columns=['Thresholds const values'])
threshold_and_values_df


##Dividend tax rates dictionarry and dataframe
dividends_tax_rates_dict = {thresholds_names_array[i]:
    {
    'Thresholds const values': THRESHOLDS_VALUES[i],
    'Tax rates':dividends_tax_rates[i]
    } for i in range(0,                             #exclude Annual Exempt Amount	[0]
        len(thresholds_names_array))
}
##print dict
print(dumps(dividends_tax_rates_dict,indent=2, ensure_ascii=False))
#df
display(HTML("<h2>Dividends tax rates</h2>"))
dividends_tax_rates_dict_df = pd.DataFrame.from_dict(dividends_tax_rates_dict, orient='index')
dividends_tax_rates_dict_df 


#Assets Sales tax rates dictionarry and dataframe
assets_sales_tax_rate_dict = {thresholds_names_array[i]:
    {
    'Thresholds const values': THRESHOLDS_VALUES[i],
    'Tax rates':assets_sales_tax_rates[i]
    } for i in range(len(thresholds_names_array))
}
#print
print(dumps(assets_sales_tax_rate_dict,indent=2, ensure_ascii=False))
#building dataframe from threshold_dividends_tax_rates_dict
display(HTML("<h2>Assets sales Tax Rates</h2>"))
assets_sales_tax_rate_dict_df = pd.DataFrame.from_dict(assets_sales_tax_rate_dict, orient='index')
assets_sales_tax_rate_dict_df 