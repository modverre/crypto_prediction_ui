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
                            line=dict(color='firebrick', width=3)))
    fig.add_trace(go.Scatter(x=x[split_index:], y=y[split_index:], name='Predicted',
                            line=dict(color='orange', width=2)))

    fig.update_layout(title=f'{coin_name}',xaxis_title='Datetime',yaxis_title='Price (vs EUR)')
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
    return x,y,24

########################################################
def get_data(coin_name):
    # Take a look a this function. THAT'S HOW MY DATA COULD LOOK LIKE
    # {
    #   'name': 'coin_name',
    #   'data': {x:[], Dates
    #            y:[] Prices/Values
    #           },
    #   'split_index':10 ## Index at which the predicted data starts
    # }
    obj= requests.get('URL TO API /{coin_name}').json()['Data']
    print(f"Fetched data for {obj['name']}")
    ## Evenauly filter
    x= obj["data"]["x"]
    y= obj["data"]["y"]
    return x,y,obj['split_idx']
########################################################


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

#price_data = load_curr_price_data('DOGECOIN,bitcoin')

doge_x,doge_y,doge_split_index = temp_get_data('dogecoin')
samoyedcoin_x,samoyedcoin_y,samoyedcoin_split_index = temp_get_data('samoyedcoin')



#Colums division
col1, col2 = st.columns(2)

col1.subheader("Price for doge")
fig = generate_price_line_chart(doge_x,doge_y,doge_split_index,'Doge')
col1.plotly_chart(fig, use_container_width=True)

col2.subheader("Price for samoyedcoin")
fig = generate_price_line_chart(samoyedcoin_x,samoyedcoin_y,samoyedcoin_split_index,'Samoyedcoin')
col2.plotly_chart(fig, use_container_width=True)

#Price & Prediction Metrics
#st.write('''# Prediction''')
#prediction_index = st.metric(label="% change in the next 24h", value="XX.XX%")
