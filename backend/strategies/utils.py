import requests
from bs4 import BeautifulSoup
import pandas as pd
import pandas_ta
import yfinance as yf
from datetime import datetime, timedelta

COLUMN_MAPPING = {'Symbol': 'Name', 
                  'rsf': 'Symbol', 
                  '1d': 'rsf', 
                  '5d': '1d', 
                  '1mo': '5d',
                  '3mo': '1mo', 
                  '6mo': '3mo', 
                  '1yr': '6mo', 
                  'vol-21': '1yr', 
                  'test': 'vol-21'}

def scrape(run: bool):
    if run:
        url = "https://www.etfscreen.com/performance.php?wl=0&s=Rtn-1mo%7Cdesc&t=6&d=i&ftS=yes&ftL=yes&vFf=dolVol21&vFl=gt&vFv=1000000&udc=default&d=i"
        response = requests.get(url=url)
        if response.status_code != 200:
            print(f"Error in getting response: {response.status_code}")
            return None
        soup = BeautifulSoup(response.content, "html.parser")
        ptbl_div = soup.find('div', class_="ptbl")
        data_list = []
        if ptbl_div:
            table = ptbl_div.find('table', class_="ptbl")
            if table:
                tr_elements = table.find_all("tr")
                for tr in range(len(tr_elements)):
                    curr_row = tr_elements[tr]
                    td_elements = curr_row.find_all("td")
                    data_dict = {}
                    for i, key in enumerate(['Name', 'Symbol', 'rsf', '1d', '5d', '1mo', '3mo', '6mo', '1yr', 'vol-21', 'test']):
                        if i < len(td_elements):
                            data_dict[key] = td_elements[i].text.strip()
                    data_list.append(data_dict)
        df = pd.DataFrame.from_dict(data_list)
        df.to_csv('data.csv')
    return None


def preprocess(df: pd.DataFrame):
    # Remove the top rows due to being empty
    df = df.drop(index=[0, 1])
    # Filter out extra columns
    df = df.drop(columns=["Name", "Unnamed: 0"])
    # Rename columns
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    # Get rid of all vix and etn tickers
    df = df[~df['Name'].str.contains('vix', case=False)]
    df = df[~df['Name'].str.contains('etn', case=False)]
    return df

def get_prices(df):
    # grab all tickers
    ticker_list = df['Symbol'].tolist()
    data = yf.download(tickers=ticker_list, start=datetime.today() - timedelta(days=365), end=datetime.today())
    data = data.stack().reset_index().rename(index=str, columns={"level_1": "Ticker"}).sort_values(['Ticker', 'Date'])
    data.set_index('Date', inplace=True)
    data.to_csv('prices.csv')

# scrape(run=False)
# data = pd.read_csv('/Users/blakedickerson/portfolio_pilot/data.csv')
# data = preprocess(data)
# get_prices(data)
