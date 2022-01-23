import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np 
import time
import matplotlib.pyplot as plt 
import datetime as dt


# Scraping Yield Curve from treasury site

url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/TextView.aspx?data=yieldYear&year=2021'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'lxml')

table_list = []

table1 = soup.find('table', class_='t-chart')

header_rows = table1.find_all('th')
header_list = []
table_rows = []
for each_th in header_rows:
	header_list.append(each_th.text)

tb_rows = table1.find_all('tr')
for each_row in tb_rows:
	row = each_row.find_all('td')
	row_text = [i.text for i in row]
	table_rows.append(row_text)
table_rows.pop(0)

table_rows.insert(0, header_list)

df = pd.DataFrame(table_rows, columns=table_rows[0])
df = df[1:]
df = df.astype({'2 yr': float, '5 yr': float, '10 yr': float, '20 yr': float, '30 yr': float})
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%y')




#scrape pmi data from ycharts.com

pmi_url = 'https://ycharts.com/indicators/us_pmi'
pmi_r = requests.get(pmi_url, headers={'User-Agent': 'Mozilla/5.0'})
pmi_soup = BeautifulSoup(pmi_r.text, 'lxml')

pmi_table_list = []


pmi_table1 = pmi_soup.find_all('td', class_='text-right')

for each in pmi_table1:
	pmi_table_list.append(each.text.strip())

pmi_table_list = pmi_table_list[:-16]
pmi_table_list2 = [float(each) for each in pmi_table_list]

dates = []
dates2 = []


date_table = pmi_soup.find_all('table', class_="table")[5]
tb_rows = date_table.find_all('tr')
for each_row in tb_rows:
	row = each_row.find('td')
	if row != None:
		dates.append(row.text)

date_table2 = pmi_soup.find_all('table', class_="table")[6]
tb_rows2 = date_table2.find_all('tr')
for each_row in tb_rows2:
	row = each_row.find('td')
	if row != None:
		dates2.append(row.text)

dates3 = dates + dates2
prepared_data = {'Dates': dates3, 'PMI': pmi_table_list2}
pmi_df = pd.DataFrame(prepared_data)
pmi_df['Dates'] = pd.to_datetime(pmi_df['Dates'], format="%B %d, %Y")






fig, (ax1, ax2) = plt.subplots(2)

ax1.plot(df['Date'], df['2 yr'], label='2 yr')
#ax1.plot(df['Date'], df['5 yr'], label='5 yr')
ax1.plot(df['Date'], df['10 yr'], label='10 yr')
#ax1.plot(df['Date'], df['20 yr'], label='20 yr')
#ax1.plot(df['Date'], df['30 yr'], label='30 yr')

ax1.legend(loc=3)
ax1.set_title('Yield Curve')


ax2.plot(pmi_df['Dates'], pmi_df['PMI'], label='PMI')
ax2.legend()
ax2.set_title('PMI')
ax2.axhline(y=50, color='red', linestyle='dashed')

plt.xticks(rotation=45)
plt.subplots_adjust(wspace=.35, hspace=.75)
plt.show()

