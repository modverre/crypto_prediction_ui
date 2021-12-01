import requests
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from datetime import datetime, timedelta

# Coins list
tickerlist = [
    'doge', 'samo', 'cummies', 'dinu', 'doggy', 'elon', 'ftm', 'grlc', 'hoge',
    'lowb', 'shib', 'shibx', 'smi', 'wow', 'yooshi', 'yummy'
]

# reduce the len of the list just for testing
#tickerlist = ['doge', 'samo']

# knit the ticker together, seperated by commas, thats how the endpoint wants the data
coin_query = ','.join(tickerlist)
hoursback = 2

url_hist = f'https://cryptov1-x3jub72uhq-ew.a.run.app/get/coin_history?tickerlist={coin_query}&hoursback={hoursback}'
response = requests.get(url_hist).json()

# get historical prices
dfs_history = {}
for coin in response:
    df = pd.DataFrame.from_dict(response[coin])
    dfs_history[coin] = df

# get predicted prices
predictions= {}
for i in tickerlist:
    preds = []
    for x in range (24):
        preds.append(np.random.uniform())
    predictions[i] = preds

# put the name and the percentage in a dict
ranking = {}
for ticker in dfs_history:
    current_price = dfs_history[ticker].tail(1)['price'][0] # last entry in the df
    last_prediction = predictions[ticker][-1]               # last entry in the list
    ranking[ticker]=(last_prediction-current_price)/current_price*100 # rounded percentage

# rank the dict
ranking = dict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))


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


#current_price_per_coin={coin:float(df_dict[coin][df_dict[coin]["timestamp"] == df_dict[coin].max()["timestamp"]]["price"]) for coin in df_dict}


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
for i,ticker in enumerate(ranking):
    i=1+i
    cols = st.columns(layout)
    # name
    cols[0].markdown(f'## {ticker}')
    # current price
    current_price = dfs_history[ticker].tail(1)['price'][0]
    cols[1].markdown(f'## €{round(current_price,8)}')
    # percentage change
    percentage_change = ranking[ticker]
    cols[2].metric(" ",f'€{round(predictions[ticker][23],8)}', f'{round(percentage_change,2)}%')
    # chart
    cols[3].line_chart(get_line_chart_data(ticker),width=100, height=120)
    st.markdown("""---""")
