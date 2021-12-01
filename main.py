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
import requests

pytrend = TrendReq()
cg = CoinGeckoAPI()

#Predicted Price in the next 24h

GCP_url = 'https://cryptov1-x3jub72uhq-ew.a.run.app/predict?coin_name=doge'

current_price_url_1 = 'https://api.coingecko.com/api/v3/simple/price?ids=dogecoin&vs_currencies=eur'
current_price_url_2 = 'https://api.coingecko.com/api/v3/simple/price?ids=samoyedcoin&vs_currencies=eur'

prediction_1 = requests.get(GCP_url).json()["prediction"]
#prediction_1 = 0.1998
prediction_2 = 0.06913

today_price_1 = requests.get(current_price_url_1).json()["dogecoin"]["eur"]
today_price_2 = requests.get(current_price_url_2).json()["samoyedcoin"]["eur"]

percent_diff_value_1 = round(((prediction_1 - today_price_1)/today_price_1) * 100, 2)
percent_diff_value_2 = round(((prediction_2 - today_price_2)/today_price_2) * 100, 2)

percent_diff_1 = f'{percent_diff_value_1}%'
percent_diff_2 = f'{percent_diff_value_2}%'

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

    fig.update_layout(xaxis_title='Datetime',yaxis_title='Price (vs EUR)')
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


#Get data from CoinGecko
def temp_get_data(coin_name):
    gecko_raw = cg.get_coin_market_chart_range_by_id(id=coin_name,
                                            vs_currency='eur',
                                            from_timestamp='1629965208',
                                            to_timestamp='1637913973'
                                            )

    x = [str(x) for x in data_make_df(gecko_raw).reset_index().datetime.values]
    y = data_make_df(gecko_raw).reset_index().price.values
    return x,y,len(x)-1

#Get data from API
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
clist = ['Dogecoin','Samoyedcoin', 'Dogelon Mars', 'Hoge Finance','Shiba Inu' ]
currency = st.selectbox("Select a coin:", clist)

#price_data = load_curr_price_data('DOGECOIN,bitcoin')

doge_x,doge_y,doge_split_index = temp_get_data('dogecoin')
samoyedcoin_x,samoyedcoin_y,samoyedcoin_split_index = temp_get_data('samoyedcoin')



#Colums division
col1, col2 = st.columns(2)

col1.markdown("""---""")
col1.subheader(clist[0])
col1.metric("Predicted Price in the next 24h", prediction_1, percent_diff_1)
col1.markdown("""---""")
col2.markdown("""---""")
col2.subheader(clist[1])
col2.metric("Predicted Price in the next 24h", prediction_2, percent_diff_2)
col2.markdown("""---""")

#Price hist & pred charts in two colums
col1.subheader("Prices from the last 3 months + Predicted Price")
fig = generate_price_line_chart(doge_x,doge_y,doge_split_index,'Doge')
col1.plotly_chart(fig, use_container_width=True)

col2.subheader("Prices from the last 3 months  + Predicted Price")
fig = generate_price_line_chart(samoyedcoin_x,samoyedcoin_y,samoyedcoin_split_index,'Samoyedcoin')
col2.plotly_chart(fig, use_container_width=True)

#Price & Prediction Metrics
#st.write('''# Prediction''')
#prediction_index = st.metric(label="% change in the next 24h", value="XX.XX%")
