# `DueTax = TaxBase * TaxRate - LessTax`
# Tax Base calculations
`B11-B13` - threshold values\
`C3` - other income\
`C4` - profit from sales\
`C11-C13 `- recursive arguments from previous tax base calculations (dividends)\
`G11-G13 `- recursive arguments from previous tax base calculations (assets sales)\
`G10` - Annual Exempt Amount for assets sales tax base calculations only

$a+b$

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


# Data to parse

`thresholds_names_array` - list of thresholds names\
`THRESHOLDS_VALUES` - const values (np.nan) - variable value calculated inside tax class\
`dividends_tax_rates` - dividend thresholds to tax rates values\
`assets_sales_tax_rates` - assets sales thresholds to tax rates values\
`annual_exempt_ammount` - assets_sales_tax tax base exempt\
`less_tax_paid_at_source` - exerpt from dividend tax\


```python
class 
```
