import requests
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

# #Load current price data for
# def load_curr_price_data(coin_names, vs_curr='eur'):
#     """This fucntion returns dict with coin names as keys and prices in vs_curr as a values
#     Args:
#         coin_name str: comma separated list of coin names i.e "bitcoin,etereum,dogecoing"
#         vs_curr (str, optional): [description]. Defaults to 'eur'.
#     Returns:
#         prices (dict): List of coin prices
#     """
#     res = {}
#     list_of_coins = [x.lower() for x in coin_names.split(',') if x ]
#     tmp = cg.get_price(ids=list_of_coins, vs_currencies=vs_curr)

#     for coin in list_of_coins:
#         price = tmp[coin]['eur']
#         res[coin]=price
#     return res

#Price chart - Plotly
def generate_price_line_chart(x, y, split_index, coin_name='COINNAME', **kwargs):
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
                             line=dict(width=2.5)))
    fig.add_trace(go.Scatter(x=x[split_index:], y=y[split_index:], name='Predicted',
                             line=dict(color='#e3cd27',width=2.5)))
    fig.update_xaxes(showgrid=False, gridwidth=0.1, gridcolor='darkgrey')
    fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='darkgrey')
    fig.update_layout(#title=f'{coin_name}',
                         #width=600,
                         height=200,
                      showlegend=False,
                        plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(t=10, l=10, b=10, r=10),
                      #xaxis_title='Datetime',

                      yaxis_title='Price (vs EUR)', **kwargs)
                      # remove facet/subplot labels
    fig.update_layout(annotations=[], overwrite=True)
    return fig


def data_make_df(raw):
    df = pd.DataFrame(raw['prices'], columns=['timestamp', 'price'])
    df2 = pd.DataFrame(raw['market_caps'], columns=['ts', 'market_caps'])
    df3 = pd.DataFrame(raw['total_volumes'], columns=['ts', 'total_volumes'])
    df['market_caps'] = df2['market_caps']
    df['total_volumes'] = df3['total_volumes']
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    df = df.set_index('datetime')

    return df


def temp_get_data(coin_name):
    gecko_raw = cg.get_coin_market_chart_range_by_id(id=coin_name,
                                                     vs_currency='eur',
                                                     from_timestamp='1637686488',
                                                     to_timestamp='1637872888'
                                                     )

    x = [str(x) for x in data_make_df(gecko_raw).reset_index().datetime.values]
    y = data_make_df(gecko_raw).reset_index().price.values
    return x, y, len(x)-1

########################################################

def get_data(coin_name):
    # Take a look a this function. THATS HOW THE DATA COULD LOOK LIKE
    # {
    #   'name': 'coin_name',
    #   'data': {
    #            x:[], Dates
    #            y:[]  Prices/Values
    #           },
    #   'split_index':10 ## Index at which the predicted data starts
    # }
    obj = requests.get('URL TO API /{coin_name}').json()['data']
    print(f"Fetched data for {obj['name']}")
    ## Evenauly filter
    x = obj["data"]["x"]
    y = obj["data"]["y"]
    return x, y, obj['split_idx']
########################################################


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

#Coin selection bar
clist = ['Dogecoin', 'Samoyedcoin'
         #'Samoyedcoin', 'Hoge Finance', 'Shiba Inu'
        ]
currency = col2.selectbox("Select a coin:", clist)

#price_data = load_curr_price_data('DOGECOIN,bitcoin')

doge_x, doge_y, doge_split_index = temp_get_data('dogecoin')
samoyedcoin_x, samoyedcoin_y, samoyedcoin_split_index = temp_get_data(
    'samoyedcoin')


#Colums division
#col1, col2 = st.columns()
# col0, col1, col2, col3 = st.columns([1,1, 1, 3])

# col1.subheader("Market Cap")
# col1.metric(label="% doge", value="XX.XX%")
# col0.markdown('# Doge')
# col0.markdown('# Samoyedcoin')
# col2.subheader("Change %")
# col2.metric(label="% doge", value="XX.XX%")
# col3.subheader("Price over time")
# fig = generate_price_line_chart(doge_x, doge_y, doge_split_index, 'Doge')
# col3.plotly_chart(fig, use_container_width=True)

# col1.metric(label="% Samoyedcoin", value="XX.XX%")
# col2.metric(label="% Samoyedcoin", value="XX.XX%")

# fig = generate_price_line_chart(samoyedcoin_x, samoyedcoin_y, samoyedcoin_split_index, 'Samoyedcoin')
# col3.plotly_chart(fig, use_container_width=True)

layout = [1,1, 1, 2]
st.title("Ranking!")
col0, col1, col2, col3 = st.columns(layout)
col1.subheader("Current Price")
col2.subheader("Predicted Price")
col3.subheader("Price over time")
for i,v in enumerate(clist):
    i=1+i
    cols = st.columns(layout)
    cols[0].markdown(f'## {v}')
    cols[1].markdown(f'## ${29*i*2},084,858')
    cols[2].metric(value=f'{(i+2) * 2 * 2} % ',label='Increase')
    if i == 0:
        fig = generate_price_line_chart(doge_x, doge_y, doge_split_index, 'Doge')
    elif i ==1:
        fig = generate_price_line_chart(samoyedcoin_x, samoyedcoin_y, samoyedcoin_split_index, 'Samoyedcoin')
    cols[3].plotly_chart(fig, use_container_width=True)

#Price & Prediction Metrics
#st.write('''# Prediction''')
#prediction_index = st.metric(label="% change in the next 24h", value="XX.XX%")
