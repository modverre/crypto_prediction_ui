import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from pytrends.request import TrendReq
from plotly import graph_objs as go
import plotly.express as px
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

import yfinance as yf

pytrend = TrendReq()
cg = CoinGeckoAPI()

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

#Page title
st.set_page_config(page_title="Crypto Predicto",
       page_icon="🤑",
       layout="wide",
    )
#Header
st.header("🤑CRYPTO PREDICTO🤑")

st.write("""
**Memes Crypto Price Prediction Based on Search and Social Data**
""")

#Coin selection bar
clist = ['Dogecoin', 'Dogelon Mars', 'Samoyedcoin', 'Hoge Finance','Shiba Inu' ]
currency = st.selectbox("Select a coin:", clist)

#Price & Prediction
st.write('''# Prediction''')
prediction_index = st.metric(label="% change in the next 24h", value="XX.XX%")
#Load Data
doge_current = cg.get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']
today = datetime.utcnow().date()

#Reformat Historical Date for next function
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = st.date_input("Date: ", value=previous_day, min_value=datetime(2014,1,1), max_value=previous_day)
ORG_USD = st.number_input("USD Amount: ", min_value=1, max_value=999999999)
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
doge_historic = cg.get_coin_history_by_id(id='dogecoin', vs_currencies='eur', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']

doge_historic = round(doge_historic, 5)

#Colum2 - Price data
st.subheader("Price data")
now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='dogecoin', vs_currency="eur", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

st.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))


#Google Trends data
st.write('''# Google Trends''')
pytrend.build_payload(kw_list=[currency])

# Interest over time
df = pytrend.interest_over_time()

#Plot Google Trends data
fig = px.line(df.reset_index(), x='date', y=currency)  #px.line(df[df['country'] == currency], x = "year", y = "gdpPercap",title = "GDP per Capita")
st.plotly_chart(fig, use_container_width=True)
