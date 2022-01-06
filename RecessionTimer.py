import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
from IPython.display import display


#Read in VIX data and ISM PMI data
vix_data = pd.read_csv('/Users/broderickbonelli/desktop/Models/^VIX(1).csv')
ism_data = pd.read_csv('/Users/broderickbonelli/desktop/Models/ISM-MAN_PMI.csv')

#convert vix_data['Date'] to datetime object
vix_data['Date'] = pd.to_datetime(vix_data['Date'], format='%Y-%m-%d')

#covert ism_data['Date'] to datetime object
ism_data['Date'] = pd.to_datetime(ism_data['Date'], format='%Y-%m-%d')

#create dataframes
df1 = pd.DataFrame(vix_data)
df1.reset_index(inplace=True, drop=True)
df1 = df1['High'].groupby(df1['Date'].dt.to_period('m')).max()



df2 = pd.DataFrame(ism_data)
df2 = df2.iloc[::-1].reset_index(drop=True)
df2 = df2['PMI'].groupby(df2['Date'].dt.to_period('m')).mean()

#merge into new df
df3 = pd.merge(df1, df2, on='Date')
df3.reset_index(inplace=True)


#conform date format so x axis charts correctly; 
date_fmt = '%Y-%m'
dt_x = [dt.datetime.strptime(str(i), date_fmt) for i in df3['Date']]
x = [mdates.date2num(i) for i in dt_x]

#resize image
plt.rcParams['figure.figsize'] = [15, 7.5]

#create figure and chart VIX and PMI w/ 'Date' as X-axis
fig, ax=plt.subplots()
ax.plot_date(x, df3['High'], linestyle='solid', color='purple', marker=',')
ax.set_ylabel('VIX Monthly High')
ax.xaxis.grid()

ax.axhline(15, color='purple', linestyle='dashed')
ax.axhline(45, color='purple', linestyle='dashed')

ax2 = ax.twinx()
ax2.plot_date(x, df3['PMI'], color='seagreen', linestyle='solid', marker=',')
ax2.set_ylabel('ISM Manufacturing PMI')

ax.legend(['VIX Monthly High'], loc=2)
ax2.legend(['ISM PMI'], loc=9)
ax2.axhline(50, color='seagreen', linestyle='dashed')


ax.axvspan(*mdates.datestr2num(['2019-08', '2019-09']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2007-05', '2007-06']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2006-06', '2007-03']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2005-12', '2006-03']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['2000-02', '2000-12']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['1998-05', '1998-07']), color='lightcoral', alpha=0.5)
ax.axvspan(*mdates.datestr2num(['1990-03', '1990-04']), color='lightcoral', alpha=0.5)

ax.set_title('Recession Timer (Red vertical highlights represent inverted Yield Curve)')

plt.show()

