# UK Tax Visualization App

## Overview
The UK Tax Visualization App is an interactive dashboard designed to help users calculate and visualize their tax liability based on the tax thresholds, rates, and various income sources. The app takes into account income from salary, profit on sales, dividends, and assets sales to compute the total tax due for an individual.

## Functionality
The app performs the following key functions:
- Calculates tax liability based on income sources and predefined tax thresholds and rates.
- Visualizes the tax breakdown for dividends and assets sales.
- Allows users to input their income values through sliders or input fields.
- Generates a bar chart showing the breakdown of tax amounts under different tax rates and thresholds.

## How to Use the App
1. **Other UK Income**: Use the slider or input field to specify the income from salary.
2. **Profit on Sales**: Use the slider or input field to enter the profit from sales.
3. **View Results**: The app will automatically calculate the tax due based on the provided income inputs and display a bar chart showing the tax breakdown.



# `DueTax = TaxBase * TaxRate - LessTax`
# Tax Base calculations
`B11-B13` - threshold values\
`C3` - other income\
`C4` - profit from sales\
`C11-C13 `- recursive arguments from previous tax base calculations (dividends)\
`G11-G13 `- recursive arguments from previous tax base calculations (assets sales)\
`G10` - Annual Exempt Amount for assets sales tax base calculations only


## Allowance
`MAX(0,B11−C3−MAX(0,(C4−100000)÷2))`                Dividends
`MAX(0,B11−C3−MAX(0,(C4−100000)÷2))`                Assets sale
## Basic
`MIN(MAX(0,B12−MAX(0,(C3−B11))),MAX(0,C4−C11))`     Dividends
`MIN(MAX(0,B12−MAX(0,(C3−B11))),MAX(0,C4−G11−G10))` Assets sale
## Higher
`MIN(MAX(0,B13−(C3−B111)),MAX(0,C4−C12−C11))`       Dividends
`MIN(MAX(0,B13−(C3−F111)),MAX(0,C4−G12−G11−G10))`   Assets sale

## Additional
`MAX(0,C4−C13−C12−C11)`                             Dividends
`MAX(0,C4−G13−G12−G11−G10)`                         Assets sale

# Tax rate is constant (see tax tables)

`thresholds_names_array` - list of thresholds names\
`dividends_tax_rates` - dividend thresholds to tax rates values\
`assets_sales_tax_rates` - assets sales thresholds to tax rates values\
`annual_exempt_ammount` - assets_sales_tax tax base exempt\
`less_tax_paid_at_source` - exerpt from dividend tax\

New ideas
