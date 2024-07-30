
try:
    from constants import (dividends_tax_rates_dict,
                        assets_sales_tax_rate_dict,
                        default_MoneyInputValue)
except ImportError:
    pass

#CALCULATIONS CORE
class OtherUkIncome:    #Income from salary input C3
    def __init__(self):
        self.value = default_MoneyInputValue
    def set(self, value):
        if isinstance(value, (int, float)):
            self.value = value
        else:
            raise ValueError("Other UK income value must be a number (int or float).")
    def excel(self, df):
        self.value = float(df.loc[1, 'Unnamed: 2'])  # parse from excel C3

class ProfitOnSales:    #Profit on sales input C4
    def __init__(self):
        self.value = default_MoneyInputValue
    def set(self, value):
        if isinstance(value,(int, float)):
            self.value = value
        else:
            raise ValueError("Profit on sales value must be a number (int or float).")
    def excel(self, df):
        self.value = float(df.loc[2, 'Unnamed: 2'])  # parse from excel C4

class PersonalAllowance:
    def __init__ (self, client, thresholds_tax_rates_and_values):
        self.client = client
        self.thresholds_tax_rates_and_values = thresholds_tax_rates_and_values
        self.personal_allowance_tax_base = 0    #C11
        self.personal_allowance_tax_due = 0
    def calculate(self):
        #MAX(0, thrld-OtherUkIncome - MAX(0,(ProfitOnSales-100000)/2))
        #MAX(0,B11−C3−MAX(0,(C4−100000)÷2))
        self.personal_allowance_tax_base = \
            max(0,
                #B11−C3−MAX(0,(C4−100000)÷2)
                    #B11 (thrld)
                (self.thresholds_tax_rates_and_values.get("Personal allowance")['Thresholds const values'] -\
                    #C3  (OtherUkIncome)
                    self.client.OtherUkIncome.value) - \
                    #MAX(0,(C4−100000)÷2)
                    max(0,
                        #(C4-100000)/2 (ProfitOnSales-100000)/2
                        (self.client.ProfitOnSales.value - 100000)/2
                        )
                )
        self.personal_allowance_tax_due = self.personal_allowance_tax_base*\
            self.thresholds_tax_rates_and_values.get("Personal allowance")['Tax rates']

class BasicRate:
    def __init__ (self, client, personal_allowance_tax_base,
                  annual_exempt_amount, thresholds_tax_rates_and_values):
        self.client = client
        self.personal_allowance_tax_base = personal_allowance_tax_base  #C11
        self.annual_exempt_amount = annual_exempt_amount
        self.thresholds_tax_rates_and_values = thresholds_tax_rates_and_values
        self.basic_rate_tax_base = 0
        self.basic_rate_tax_due = 0
    def calculate(self):
        #MIN(MAX(0, thrld - MAX(0, (OtherUkIncome-PersonalAllwnceThrld))),MAX(0,(PrftOnSales-PesonalAllwnce_tax_base))
        #MIN(MAX(0,B12−MAX(0,(C3−B11))),MAX(0,C4−C11))
        self.basic_rate_tax_base = \
            min(#1-st value
                    #MAX(0, B12 − MAX(0,(C3−B11))),
                max(0,
                    #B12 − MAX(0,(C3−B11)))
                    self.thresholds_tax_rates_and_values.get("Basic rate taxpayer threshold")['Thresholds const values']-\
                        #MAX(0,(C3−B11))
                    max(0,
                            #C3-B11
                        self.client.OtherUkIncome.value - self.thresholds_tax_rates_and_values.get("Personal allowance")['Thresholds const values']
                    )
                ),
                #2-nd value
                    #MAX(0,C4−C11))
                max(0,
                        #C4−C11-(annual_exempt_amount)
                    self.client.ProfitOnSales.value - self.personal_allowance_tax_base\
                        - self.annual_exempt_amount
                )
            )

        self.basic_rate_tax_due = self.basic_rate_tax_base*\
            self.thresholds_tax_rates_and_values.get("Basic rate taxpayer threshold")['Tax rates']

class HigherRate:
    def __init__ (self, client, personal_allowance_tax_base,
                  basic_rate_tax_base,annual_exempt_amount,
                  thresholds_tax_rates_and_values):
        self.client = client
        self.personal_allowance_tax_base = personal_allowance_tax_base  #C11
        self.basic_rate_tax_base = basic_rate_tax_base                  #C12
        self.annual_exempt_amount = annual_exempt_amount
        self.thresholds_tax_rates_and_values = thresholds_tax_rates_and_values
        self.higher_rate_tax_base = 0
        self.higher_rate_tax_due = 0
    def calculate(self):
        #MIN(MAX(0,B13−(C3−B111)),MAX(0,C4−C12−C11))
        self.higher_rate_tax_base = \
            min(#1-st value
                #MAX(0,B13−(C3−B111))
                max(0,
                    #B13−(C3−B111) SET B111 = 0 what is B11?
                    self.thresholds_tax_rates_and_values.get("Higher rate threshold")['Thresholds const values']-\
                        (self.client.OtherUkIncome.value - 0)
                        #B11?? self.thresholds_tax_rates_and_values.get("Personal allowance")['Thresholds const values']
                ),
                #2-nd value
                #MAX(0,C4−C12−C11))
                max(0,
                        #C4−C12−C11-(annual_exempt_amount)
                    self.client.ProfitOnSales.value - self.basic_rate_tax_base - self.personal_allowance_tax_base\
                        - self.annual_exempt_amount
                )
            )

        self.higher_rate_tax_due = self.higher_rate_tax_base*\
            self.thresholds_tax_rates_and_values.get("Higher rate threshold")['Tax rates']

class AdditionalRate:
    def __init__ (self, client, personal_allowance_tax_base, basic_rate_tax_base,
                  higher_rate_tax_base, annual_exempt_amount,
                  thresholds_tax_rates_and_values):
        self.client = client
        self.personal_allowance_tax_base = personal_allowance_tax_base  #C11
        self.basic_rate_tax_base = basic_rate_tax_base                  #C12
        self.higher_rate_tax_base = higher_rate_tax_base                #C13
        self.annual_exempt_amount = annual_exempt_amount
        self.thresholds_tax_rates_and_values = thresholds_tax_rates_and_values
        self.additional_rate_tax_base = 0
        self.additional_rate_tax_due = 0
    def calculate(self):
        #MAX(0,C4−C13−C12−C11)
        self.additional_rate_tax_base = max(0,
                self.client.ProfitOnSales.value -\
                self.higher_rate_tax_base -\
                self.basic_rate_tax_base - \
                self.personal_allowance_tax_base-\
                self.annual_exempt_amount
            )

        self.additional_rate_tax_due = self.additional_rate_tax_base*\
            self.thresholds_tax_rates_and_values.get("Additional rate threshold")['Tax rates']

class DividendsTax:
    annual_exempt_amount = 0
    thresholds_tax_rates_and_values = dividends_tax_rates_dict

    def __init__(self, client):
        self.client = client
        self.PersonalAllowance = PersonalAllowance(client, DividendsTax.thresholds_tax_rates_and_values)
        self.BasicRate = BasicRate(client, 0, DividendsTax.annual_exempt_amount, DividendsTax.thresholds_tax_rates_and_values)
        self.HigherRate = HigherRate(client, 0, 0, DividendsTax.annual_exempt_amount, DividendsTax.thresholds_tax_rates_and_values)
        self.AdditionalRate = AdditionalRate(client, 0, 0, 0, DividendsTax.annual_exempt_amount, DividendsTax.thresholds_tax_rates_and_values)
        self.dividends_tax_due_total = 0
        self.dividends_tax_due_before_less = 0
        self.dividends_tax_base_total = 0
        self.less_tax_paid_at_source = 0

    def calculate(self):
        self.PersonalAllowance.calculate()
        self.BasicRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.BasicRate.calculate()
        self.HigherRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.HigherRate.basic_rate_tax_base = self.BasicRate.basic_rate_tax_base
        self.HigherRate.calculate()
        self.AdditionalRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.AdditionalRate.basic_rate_tax_base = self.BasicRate.basic_rate_tax_base
        self.AdditionalRate.higher_rate_tax_base = self.HigherRate.higher_rate_tax_base
        self.AdditionalRate.calculate()
        self.dividends_tax_base_total = (self.PersonalAllowance.personal_allowance_tax_base +
                                        self.BasicRate.basic_rate_tax_base +
                                        self.HigherRate.higher_rate_tax_base +
                                        self.AdditionalRate.additional_rate_tax_base)
        self.dividends_tax_due_before_less = (self.PersonalAllowance.personal_allowance_tax_due +
                                            self.BasicRate.basic_rate_tax_due +
                                            self.HigherRate.higher_rate_tax_due +
                                            self.AdditionalRate.additional_rate_tax_due)
        self.less_tax_paid_at_source = max(-(self.dividends_tax_due_before_less), -(self.client.ProfitOnSales.value * 0.1))
        self.dividends_tax_due_total = (self.dividends_tax_due_before_less +
                                        self.less_tax_paid_at_source)
class AssetsSalesTax:
    annual_exempt_amount = 3000
    thresholds_tax_rates_and_values = assets_sales_tax_rate_dict

    def __init__(self, client):
        self.client = client
        self.PersonalAllowance = PersonalAllowance(client, AssetsSalesTax.thresholds_tax_rates_and_values)
        self.BasicRate = BasicRate(client, 0, AssetsSalesTax.annual_exempt_amount, AssetsSalesTax.thresholds_tax_rates_and_values)
        self.HigherRate = HigherRate(client, 0, 0, AssetsSalesTax.annual_exempt_amount, AssetsSalesTax.thresholds_tax_rates_and_values)
        self.AdditionalRate = AdditionalRate(client, 0, 0, 0, AssetsSalesTax.annual_exempt_amount, AssetsSalesTax.thresholds_tax_rates_and_values)
        self.assets_sales_tax_due_total = 0
        self.assets_sales_tax_base_total = 0

    def calculate(self):
        self.PersonalAllowance.calculate()
        self.BasicRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.BasicRate.calculate()
        self.HigherRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.HigherRate.basic_rate_tax_base = self.BasicRate.basic_rate_tax_base
        self.HigherRate.calculate()
        self.AdditionalRate.personal_allowance_tax_base = self.PersonalAllowance.personal_allowance_tax_base
        self.AdditionalRate.basic_rate_tax_base = self.BasicRate.basic_rate_tax_base
        self.AdditionalRate.higher_rate_tax_base = self.HigherRate.higher_rate_tax_base
        self.AdditionalRate.calculate()
        self.assets_sales_tax_base_total = (
            self.PersonalAllowance.personal_allowance_tax_base +
            self.BasicRate.basic_rate_tax_base +
            self.HigherRate.higher_rate_tax_base +
            self.AdditionalRate.additional_rate_tax_base+
            self.annual_exempt_amount
        )
        self.assets_sales_tax_due_total = (
            self.PersonalAllowance.personal_allowance_tax_due +
            self.BasicRate.basic_rate_tax_due +
            self.HigherRate.higher_rate_tax_due +
            self.AdditionalRate.additional_rate_tax_due
        )

class Client:           #Client class
    def __init__(self, name):
        self.name = name
        self.OtherUkIncome = OtherUkIncome()
        self.ProfitOnSales = ProfitOnSales()
        self.DividendsTax = DividendsTax(self)
        self.AssetsSalesTax = AssetsSalesTax(self)
