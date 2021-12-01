import requests
import streamlit as st
import pandas as pd
import numpy as np
from params import COIN_TRANSLATION_TABLE
import datetime as datetime
from plotly import graph_objs as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"  # change plotly default, white looks better

# Coins list
tickerlist = [
    'doge', 'samo', 'cummies', 'dinu', 'doggy', 'elon', 'ftm', 'grlc', 'hoge',
    'lowb', 'shib', 'shibx', 'smi', 'wow', 'yooshi', 'yummy'
]
hoursback = 48

# reduce the len of the list just for testing
#tickerlist = ['doge', 'samo']
#hoursback = 20

# knit the ticker together, seperated by commas, thats how the endpoint wants the data
coin_query = ','.join(tickerlist)

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

# fake data for the predictions
timestamp = total_volumes = market_caps = [0] * 24
# make the whole dataframe with index and history + predictions
dfs_full = {}
for ticker in tickerlist:
    # make df with fake-data and prediction price
    add = {'market_caps':market_caps,'price':predictions[ticker],'timestamp':timestamp,'total_volumes':total_volumes}
    add = pd.DataFrame.from_dict(add)
    # append it to the history
    df = dfs_history[ticker].append(add)
    # now the index is fucked (history = hourly datetime, predictions = 0..23), we have to fix that
    start = df.index[0]  # = first date
    start_dt = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc) # date to datetime
    df.index = pd.date_range(start_dt, periods=df.shape[0],freq="H") # hourly data from beginning to end
    dfs_full[ticker] = df

#Line chart
def get_line_chart_data(coin_name):
    return pd.DataFrame(predictions[coin_name],columns=['Predicted price'])

def generate_price_line_chart(x,y,split_index,coin_name='COINNAME'):
    """This function generates a plotly line chart (plotly.go).
    Args:
        x ([list]): [description]
        y ([list]): [description]
        split_index ([type]): where the predicted data starts
        coin_name (str, optional): [description]. Defaults to 'COINNAME'.

    Returns:
        figure
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x[0:split_index+1], y=y[0:split_index+1], name='Historical',
                            line=dict(color='firebrick', width=2)))
    fig.add_trace(go.Scatter(x=x[split_index:], y=y[split_index:], name='Predicted',
                            line=dict(color='orange', width=2)))

    fig.update_layout(xaxis_title='Datetime',yaxis_title='Price (vs EUR)',
                      width=500, height=200, margin=dict(l=0, r=0, t=0, b=0),
                      autosize=False)
    return fig


#
# bigger calculations ends here
# ------------------------------------------------------------------------------
# design starts here
#

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
    coin_name = COIN_TRANSLATION_TABLE[ticker]['display']
    cols[0].markdown(f'## {coin_name}')
    # current price
    current_price = dfs_history[ticker].tail(1)['price'][0]
    current_marketcap = dfs_history[ticker].tail(1)['market_caps'][0]
    cols[1].markdown(f'## €{round(current_price,8)}')
    cols[1].markdown('market cap')
    cols[1].markdown(f'## €{int(current_marketcap):,}')



    # percentage change
    percentage_change = ranking[ticker]
    cols[2].metric(" ",f'€{round(predictions[ticker][23],8)}', f'{round(percentage_change,2)}%')
    # chart
    #cols[3].line_chart(get_line_chart_data(ticker),width=100, height=120)
    fig = generate_price_line_chart(dfs_full[ticker].index, dfs_full[ticker]['price'], 24, coin_name=coin_name)
    cols[3].plotly_chart(fig #use_container_width=True
                         )
    st.markdown("""---""")
