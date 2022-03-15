# %%
import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for 
import math #The Python math module
from scipy import stats #The SciPy stats module

# %%
stocks = pd.read_csv('sp_500_stocks.csv')
from secrets import IEX_CLOUD_API_TOKEN

# %%
# Function sourced from 
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]   
        
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

data = {}
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data.update(requests.get(batch_api_call_url).json())



# %%
my_columns = ['Ticker', 'Price', 'One-Year Price Return', 'Number of Shares to Buy']

iex_cols = {
    'Price': ['quote','latestPrice'],
    'One-Year Price Return': ['stats', 'year1ChangePercent']
}

final_dataframe = pd.DataFrame(columns = my_columns)
final_dataframe['Ticker'] = stocks['Ticker']

for key in iex_cols.keys():
    tmp_series = []
    for stock in stocks['Ticker']:
        tmp_series.append(data[stock][iex_cols[key][0]][iex_cols[key][1]])
    final_dataframe[key] = tmp_series

# %%
final_dataframe

# %%
final_dataframe.sort_values('One-Year Price Return', ascending = False, inplace = True)
final_dataframe = final_dataframe[:51]
final_dataframe.reset_index(drop = True, inplace = True)
final_dataframe

# %%
def portfolio_input():
    global portfolio_size
    portfolio_size = input("Enter the value of your portfolio:")

    try:
        val = float(portfolio_size)
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_size = input("Enter the value of your portfolio:")

portfolio_input()

# %%
position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size / final_dataframe['Price'][i])
final_dataframe

# %%
hqm_columns = [
                'Ticker', 
                'Price', 
                'Number of Shares to Buy', 
                'One-Year Price Return', 
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]

hqm_iex_cols = {
                'Price': ['quote','latestPrice'],       
                'One-Year Price Return': ['stats', 'year1ChangePercent'],
                'Six-Month Price Return': ['stats', 'month6ChangePercent'],
                'Three-Month Price Return': ['stats', 'month3ChangePercent'],
                'One-Month Price Return': ['stats', 'month1ChangePercent'] 
}

hqm_dataframe = pd.DataFrame(columns = hqm_columns)
hqm_dataframe['Ticker'] = stocks['Ticker']

for key in hqm_iex_cols.keys():
    tmp_series = []
    for stock in stocks['Ticker']:
        tmp_series.append(data[stock][hqm_iex_cols[key][0]][hqm_iex_cols[key][1]])
    hqm_dataframe[key] = tmp_series




# %%
time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

for time_period in time_periods:
    tmp_series = []
    for row in hqm_dataframe.index:
        tmp_percentile = stats.percentileofscore(hqm_dataframe[f'{time_period} Price Return'], hqm_dataframe.loc[row, f'{time_period} Price Return'])/100
        tmp_series.append(tmp_percentile)
    hqm_dataframe[f'{time_period} Return Percentile'] = tmp_series

hqm_dataframe

# %%
from statistics import mean

for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)

hqm_dataframe.sort_values(by = 'HQM Score', ascending = False)
hqm_dataframe = hqm_dataframe[:51]

hqm_dataframe

# %%



