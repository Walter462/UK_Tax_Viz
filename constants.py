try: 
  from IMPORT import np
except ImportError:
    pass 
  
dividends_tax_rates_dict = {    #constants(thresholds and tax rates) for dividend tax
    "Personal allowance": {
        "Thresholds const values": 12570.0,
        "Tax rates": 0.0
    },
    "Basic rate taxpayer threshold": {
        "Thresholds const values": 37700.0,
        "Tax rates": 0.0875
    },
    "Higher rate threshold": {
        "Thresholds const values": 125140.0,
        "Tax rates": 0.3375
    },
    "Additional rate threshold": {
        "Thresholds const values": np.NaN,
        "Tax rates": 0.3935
    }
}

assets_sales_tax_rate_dict = {  #constants(thresholds and tax rates) for assets sales tax
  "Personal allowance": {
    "Thresholds const values": 12570.0,
    "Tax rates": 0.0
  },
  "Basic rate taxpayer threshold": {
    "Thresholds const values": 37700.0,
    "Tax rates": 0.1
  },
  "Higher rate threshold": {
    "Thresholds const values": 125140.0,
    "Tax rates": 0.2
  },
  "Additional rate threshold": {
    "Thresholds const values": np.NaN,
    "Tax rates": 0.2
  }
}

default_MoneyInputValue = 0     #user default input constant for client income/profit

