# %%
import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for 
import math #The Python math module
from scipy import stats #The SciPy stats module

stocks = pd.read_csv('sp_500_stocks.csv')
from secrets import IEX_CLOUD_API_TOKEN

# %%
symbol_groups = [list(stocks.Ticker)[x:x+100] for x in range(0, len(list(stocks.Ticker)), 100)]
symbol_strings = [(',').join(i) for i in symbol_groups]

# %%
def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the value of your portfolio:")

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio:")

# %%
rv_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy', 
    'Price-to-Earnings Ratio',
    'PE Percentile',
    'Price-to-Book Ratio',
    'PB Percentile',
    'Price-to-Sales Ratio',
    'PS Percentile',
    'EV/EBITDA',
    'EV/EBITDA Percentile',
    'EV/GP',
    'EV/GP Percentile',
    'RV Score'
]

rv_dataframe = pd.DataFrame(columns = rv_columns)
rv_dataframe['Ticker'] = stocks['Ticker']

# %%
data = {}
for s in symbol_strings:
    batch_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={s}&types=quote,advanced-stats&token={IEX_CLOUD_API_TOKEN}'
    data.update(requests.get(batch_url).json())

# %%
rv_dict = {
    'Price': ['quote', 'latestPrice'],
    'Price-to-Earnings Ratio': ['quote', 'peRatio'],
    'Price-to-Book Ratio': ['advanced-stats', 'priceToBook'],
    'Price-to-Sales Ratio': ['advanced-stats', 'priceToSales'],
    'enterprise_value': ['advanced-stats', 'enterpriseValue'],
    'ebitda': ['advanced-stats', 'EBITDA'],
    'gross_profit': ['advanced-stats', 'grossProfit']
}

for k in rv_dict.keys():
    tmp = []
    for s in stocks['Ticker']:
        tmp.append(data[s][rv_dict[k][0]][rv_dict[k][1]])
    rv_dataframe[k] = tmp

# %%

for row in rv_dataframe.index:
        try:
            rv_dataframe.loc[row, 'EV/EBITDA']  = rv_dataframe['enterprise_value'][row]/rv_dataframe['ebitda'][row]
        except TypeError:
            rv_dataframe.loc[row, 'EV/EBITDA']  = np.NaN

        try:
            rv_dataframe.loc[row, 'EV/GP']  = rv_dataframe['enterprise_value'][row]/rv_dataframe['gross_profit'][row]
        except TypeError:
            rv_dataframe.loc[row, 'EV/GP']  = np.NaN
        
            

# %%
for column in ['Price-to-Earnings Ratio', 'Price-to-Book Ratio','Price-to-Sales Ratio',  'EV/EBITDA','EV/GP']:
    rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace = True)

# %%
metrics = {
            'Price-to-Earnings Ratio': 'PE Percentile',
            'Price-to-Book Ratio':'PB Percentile',
            'Price-to-Sales Ratio': 'PS Percentile',
            'EV/EBITDA':'EV/EBITDA Percentile',
            'EV/GP':'EV/GP Percentile'
}

for row in rv_dataframe.index:
    for metric in metrics.keys():
        rv_dataframe.loc[row, metrics[metric]] = stats.percentileofscore(rv_dataframe[metric], rv_dataframe.loc[row, metric])/100

# %%
from statistics import mean

for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]])
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)

# %%
rv_dataframe.sort_values(by = 'RV Score', ascending=False, inplace = True)
rv_dataframe = rv_dataframe[:50]
rv_dataframe.reset_index(drop = True, inplace = True)

# %%
portfolio_input()

# %%
position_size = float(portfolio_size) / len(rv_dataframe.index)
for i in range(0, len(rv_dataframe['Ticker'])-1):
    rv_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / rv_dataframe['Price'][i])

# %%
rv_dataframe

# %%



