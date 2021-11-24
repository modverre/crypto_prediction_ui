import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pytrends.request import TrendReq
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta


pytrend = TrendReq()
cg = CoinGeckoAPI()

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

#Load Data
doge_current = cg.get_price(ids='dogecoin', vs_currencies='usd')['dogecoin']['usd']
today = datetime.utcnow().date()
#doge_market_cap = cg.get_coin_market_chart_by_id(id='dogecoin', vs_currency='usd', days=1, interval="daily")
doge_market_cap_current = cg.get_coin_market_chart_by_id(id='dogecoin', vs_currency='eur', days=1, interval="daily")
date_market_cap = doge_market_cap_current['market_caps'][0][0]


#Coin selection bar
clist = ['Dogecoin', 'Dogelon Mars', 'Samoyedcoin', 'Hoge Finance','Shiba Inu' ]
currency = st.selectbox("Select a coin:", clist)

#Sidebar
add_selectbox = st.sidebar.title(currency)
image = st.sidebar.image("/Users/nat.walentynowicz/Downloads/image.png", width=250)
market_cap_string = "${}".format(date_market_cap)
marketcap = st.sidebar.metric(label="Market Capitization", value=market_cap_string)
age = st.sidebar.markdown("**How old is the coin:**")
overall_sen = st.sidebar.markdown("**Overall Sentiment:**")


#Colums division
col1, col2 = st.columns(2)

#Price & Prediction
col1.write('''# Results''')
coin_price_string = "${}".format(doge_current)
prediction_index = col1.metric(label="% change in the next 24h", value="XX.XX%")
price_index = col1.metric(label="Current Price", value=coin_price_string)


# Custom function for rounding values
#def round_value(input_value):
    #if input_value.values > 1:
        #a = float(round(input_value, 2))
    #else:
        #a = float(round(input_value, 8))
    #return a


#Reformat Historical Date for next function
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)
HIST_DATE = col2.date_input("Date: ", value=previous_day, min_value=datetime(2014,1,1), max_value=previous_day)
ORG_USD = col2.number_input("USD Amount: ", min_value=1, max_value=999999999)
HIST_DATE_REFORMAT = HIST_DATE.strftime("%d-%m-%Y")
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT,"%d-%m-%Y")
doge_historic = cg.get_coin_history_by_id(id='dogecoin', vs_currencies='usd', date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']

doge_historic = round(doge_historic, 5)

#Colum2 - Price data
col2.subheader("Price data")
now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id='dogecoin', vs_currency="usd", from_timestamp=HIST_DATE_datetime.timestamp(), to_timestamp=now.timestamp())['prices']

dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {"Prices":prices, "Dates":dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],unit='ms',origin='unix')

col2.line_chart(df.rename(columns={"Dates":"index"}).set_index("index"))

#Google Trends
st.subheader("Google Trends")
pytrend.build_payload(kw_list=[currency])

# Interest by Region
df = pytrend.interest_over_time()

fig = px.line(df.reset_index(), x='date', y=currency)  #px.line(df[df['country'] == currency], x = "year", y = "gdpPercap",title = "GDP per Capita")
st.plotly_chart(fig, use_container_width=True)

#col2.subheader("A narrow column with the data")
#col2.table(df.sort_values(by=currency, ascending=False))
