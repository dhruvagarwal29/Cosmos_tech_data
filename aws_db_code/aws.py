from bs4 import BeautifulSoup
import requests
import pandas as pd
import boto3
from io import StringIO

ua = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"}
web = 'https://www.coingecko.com/en'
resp = requests.get(web)
soup = BeautifulSoup(resp.content, 'html.parser')
res = soup.find('table', {'class':'table-scrollable'}).find('tbody').find_all('tr')


# taking the names of currencies

name_currency = []


for result in res:
    
    # name
    try:
        name_currency.append(result.find('a', {'class':'lg:tw-flex font-bold tw-items-center tw-justify-between'}).get("href").split('/')[-1])

    except:
        name_currency.append('n/a')

name_currency



""" ### From start of the year"""

# empty list
name = []
date = []
market_cap = []
volume = []
open = []
close = []
for j in range(len(name_currency)):
  name1 = name_currency[j]
  print(name1)
  for i in range(1,2):
    # website
    website= f'https://www.coingecko.com/en/coins/{name1}/historical_data?end_date=2022-07-12&page={i}&start_date=2022-01-01'
    #print (website)
    # request to website
    response = requests.get(website)

    # soup object
    soup = BeautifulSoup(response.content, 'html.parser')

    # results
    results = soup.find('table', {'class':'table table-striped text-sm text-lg-normal'}).find('tbody').find_all('tr') 

    for result in results:
      # name
      name.append(name1)
      # date
      try:
          date.append(result.find('th', {'class':'font-semibold text-center'}).get_text().strip()) 
      except:
          date.append('n/a')
      headings = []
      for td in result.find_all("td"):
          # remove any newlines and extra spaces from left and right
          headings.append(td.text.replace('\n', ' ').strip())

          #print(headings[0])
          #print(headings[1])
          #print(headings[2])
          #print(headings[3])
      #  market cap 
      try:
        market_cap.append(headings[0])
      except:
        market_cap.append('n/a')
      # volume
      try:
          volume.append(headings[1])
      except:
          volume.append('n/a')
      
      # open
      try:
          open.append(headings[2])
      except:
          open.append('n/a')
          
      # close
      try:
          close.append(headings[3])
      except:
          close.append('n/a')

# create dataframe
crypto = pd.DataFrame({'Coin': name, 'Date':date, 'Market cap':market_cap,
                                'Volume': volume, 'Open': open, 'Close': close,})

# output dataframe
crypto

#drop rows that contain N/A in the list
crypto = crypto[crypto.Close != 'N/A']
#crypto.to_csv('crypto_histo.csv')

crypto.to_csv("s3://cosmos-metaverse/crypto_new.csv",
          storage_options={'key': 'Key',
                           'secret': 'Secret'})

print("Dataframe is saved as CSV in S3 bucket.")
