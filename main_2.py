import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime, timedelta
import requests

#Coins list
clist = ["doge", "shib", "elon", "samo", "hoge",
         "mona", "dogedash", "erc20", "ban", "cummies",
         "doggy",  "smi", "doe", "pepecash","wow",
         "dinu", "yummy", "shibx", "lowb", "grlc"]

#price_data = load_curr_price_data('DOGECOIN,bitcoin')

#Test data for front-end
def data_make_df(raw):
    df = pd.DataFrame(raw['prices'], columns=['timestamp', 'price'])
    df2 = pd.DataFrame(raw['market_caps'], columns=['ts', 'market_caps'])
    df3 = pd.DataFrame(raw['total_volumes'], columns=['ts', 'total_volumes'])
    df['market_caps'] = df2['market_caps']
    df['total_volumes'] = df3['total_volumes']
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    df = df.set_index('datetime')

    return df


#Page title
st.set_page_config(page_title="Crypto Predicto",
                   page_icon="🤑",
                   layout="wide",
                   )

col1, col2= st.columns([3,1])

#Header
col1.header("🤑CRYPTO PREDICTO🤑")

col1.write("""
Memes Crypto Price Prediction Based on Search and Social Data
""")

#Line chart
def get_line_chart_data():

    return pd.DataFrame(
            np.random.randn(20, 1),
            columns=['Price hourly']
        )

df = get_line_chart_data()

#Ranking
st.markdown("""---""")
layout = [1,1, 1, 2]
col0, col1, col2, col3 = st.columns(layout)

#Current Price
col1.subheader("*Current Price*")
#Predicted Price & % change
col2.subheader("*Predicted Price*")
#Predicted Price for next 24h
col3.subheader("*Predicted Price next 24h*")
st.markdown("""---""")

#Filling the columns
for i,v in enumerate(clist):
    i=1+i
    cols = st.columns(layout)
    cols[0].markdown(f'## {v}')
    cols[1].markdown(f'## ${29*i*2},084,858')
    cols[2].metric(v,"$121.10", "0.46%")
    cols[3].line_chart(df)
    st.markdown("""---""")


#Historial prices from our API
url_hist = 'https://cryptov1-x3jub72uhq-ew.a.run.app/get/coin_history?tickerlist=doge,samo&hoursback=3'

response = requests.get(url_hist).json()
df_dict = {}
for coin in response:
    df = pd.DataFrame.from_dict(response[coin])
    df_dict[coin] = df

current_price_per_coin={coin:float(df_dict[coin][df_dict[coin]["timestamp"] == df_dict[coin].max()["timestamp"]]["price"]) for coin in df_dict}

# for coin in response:
#     df = pd.DataFrame.from_dict(response[coin])
#     df_list.append(df)

# df_list

# #Prediciton prices from our API
# import requests
# import pandas as pd

# GCP_url = 'https://cryptov1-x3jub72uhq-ew.a.run.app/predict?coin_name=doge'

# current_price_url_1 = 'https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=eur'
# current_price_url_2 = 'https://api.coingecko.com/api/v3/simple/price?ids=samoyedcoin&vs_currencies=eur'

# prediction_1 = requests.get(GCP_url).json()["prediction"]
# #prediction_1 = 0.1998
# prediction_2 = 0.06913

# today_price_1 = requests.get(current_price_url_1).json()["dogecoin"]["eur"]
# today_price_2 = requests.get(current_price_url_2).json()["samoyedcoin"]["eur"]

# percent_diff_value_1 = round(((prediction_1 - today_price_1)/today_price_1) * 100, 2)
# percent_diff_value_2 = round(((prediction_2 - today_price_2)/today_price_2) * 100, 2)

# percent_diff_1 = f'{percent_diff_value_1}%'
# percent_diff_2 = f'{percent_diff_value_2}%'
