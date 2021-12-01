import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime, timedelta

#Coins list
clist = ['doge','samo','cummies','dinu','doggy','elon',
         'ftm','grlc','hoge','lowb','shib',
         'shibx','smi','wow','yooshi','yummy']

#price_data = load_curr_price_data('DOGECOIN,bitcoin')

#Page configuration
st.set_page_config(page_title="Crypto Predicto",
                   page_icon="🦈",
                   layout="wide",
                   )

#Header

col1, col2= st.columns([1,3])

col1.image("https://xdisplays.net/priv/crypto_logo.png", width=200)

col2.markdown("""
### Memes Crypto Price Prediction Based on Search and Social Data
""")

col2.selectbox("Select a coin:", clist)

#Historial prices from our API
url_hist = 'https://cryptov1-x3jub72uhq-ew.a.run.app/get/coin_history?tickerlist=doge,samo&hoursback=3'

response = requests.get(url_hist).json()
df_dict = {}
for coin in response:
    df = pd.DataFrame.from_dict(response[coin])
    df_dict[coin] = df

current_price_per_coin={coin:float(df_dict[coin][df_dict[coin]["timestamp"] == df_dict[coin].max()["timestamp"]]["price"]) for coin in df_dict}


#Predicted prices
list_of_dfs = ['doge','samo','cummies','dinu','doggy','elon',
         'ftm','grlc','hoge','lowb','shib',
         'shibx','smi','wow','yooshi','yummy']

predictions= {}

for i in list_of_dfs:
    preds = []
    for x in range (24):
        preds.append(np.random.uniform())
    predictions[i] = preds

#Line chart
def get_line_chart_data(coin_name):

    return pd.DataFrame(predictions[coin_name],columns=['Predicted price'])


# for coin in response:
#     df = pd.DataFrame.from_dict(response[coin])
#     df_list.append(df)

# df_list


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
    cols[1].markdown(f'## €{round(current_price_per_coin[v],8)}')
    percent_diff_value = round(((predictions[v][23] - current_price_per_coin[v])/current_price_per_coin[v]) * 100)
    cols[2].metric(" ",f'€{round(predictions[v][23],8)}', f'{percent_diff_value}%')
    cols[3].line_chart(get_line_chart_data(v),width=60, height=50)
    st.markdown("""---""")

list_of_dfs = ["ban", "cummies", "dinu", "doge",
"doggy", "elon", "erc20", "ftm", "grlc", "hoge",
"lowb", "mona", "samo", "shib", "shibx", "smi",
"wow", "yooshi","yummy"]
