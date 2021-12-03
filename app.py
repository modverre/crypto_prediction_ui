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

# the waves
# https://codepen.io/andyfitz/pen/akAKdV

# Coins list
tickerlist = ["ban", "cummies", "dinu", "doge",
"doggy", "elon", "erc20", "ftm", "grlc", "hoge",
"lowb", "mona", "samo", "shib", "shibx", "smi",
"wow", "yooshi","yummy"]

np.set_printoptions(suppress=True)

hoursback = 48

# reduce the len of the list just for testing
#tickerlist = ['doge', 'samo']
#hoursback = 20

# knit the ticker together, seperated by commas, thats how the endpoint wants the data
coin_query = ','.join(tickerlist)

url_hist = f'https://cryptov1-x3jub72uhq-ew.a.run.app/get/coin_history?tickerlist={coin_query}&hoursback={hoursback}'
try:
    response = requests.get(url_hist).json()
except:
    st.write('uh oh, coingecko has seen us -- abort, abort -- lets sneak back in later')
    st.stop()

# get historical prices
dfs_history = {}
for coin in response:
    df = pd.DataFrame.from_dict(response[coin])
    dfs_history[coin] = df

def get_predictions(testdata=True):
    if testdata:
        predictions= {}
        for i in tickerlist:
            preds = []
            for x in range (24):
                preds.append(np.random.uniform())
            predictions[i] = preds
    else:
        url_predict = 'https://cryptov1-x3jub72uhq-ew.a.run.app/predict'
        predictions = requests.get(url_predict).json()  # its NOT a dataframe but a dict of lists, so the call only is fine!
    return predictions

predictions = get_predictions(testdata=False)

# dirty hack ----------
predictions_adjusted = {}
for ticker in tickerlist:
    last_real_price = dfs_history[ticker].tail(1)['price'][0]
    first_prediction = predictions[ticker][0]
    gap = first_prediction - last_real_price
    predictions_adjusted[ticker] = [x - gap for x in predictions[ticker]]

predictions = predictions_adjusted
# ---------------------

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

#Line chart (old)
def get_line_chart_data(coin_name):
    return pd.DataFrame(predictions[coin_name],columns=['Predicted price'])


def generate_price_line_chart(x,y,split_index,coin_name='COINNAME',pred_color='orange'):
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
                            line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=x[split_index:], y=y[split_index:], name='Predicted',
                            line=dict(color=pred_color, width=2)))
    fig.update_layout(xaxis_title='Datetime',yaxis_title='Price (vs EUR)',
                      width=500, height=200, margin=dict(l=0, r=0, t=0, b=0),
                      autosize=False)
    ## addition from garrit
    min = y.min()
    max = y.max()

    #fig.update_yaxes(range=[min-1*min, max + 0.25 * max])
    #fig.update_yaxes(range=[min-1*min, max + 0.25 * max])

    return fig


#
# bigger calculations ends here
# ------------------------------------------------------------------------------
# design starts here
#



st.set_page_config(page_title='Cryptologix Group presents: Crypto Shark',
                   page_icon="🦈",
                   layout="wide",
                   initial_sidebar_state="collapsed",
                   menu_items=None)

# remove padding
padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        margin-top: 0;
        padding-top: 0;
        padding-right: 0;
        padding-left: 0;
        padding-bottom: 0rem;
    }} </style> """, unsafe_allow_html=True)

# load magic
HtmlFile = open("test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
st.markdown(source_code, unsafe_allow_html= True)


#Ranking
st.markdown("""---""")
layout = [1, 3, 3, 3, 6]
col0, col1, col2, col3, col4 = st.columns(layout)

#Current Price
col2.subheader("*Current Price*")
#Predicted Price & % change
col3.subheader("*Predicted Price*")
#Predicted Price for next 24h
col4.subheader("*Predicted Price next 24h*")
st.markdown("""---""")



#Filling the columns
for i,ticker in enumerate(ranking):
    i=1+i
    cols = st.columns(layout)
    # name
    coin_name = COIN_TRANSLATION_TABLE[ticker]['display']
    cols[1].markdown(f'## {coin_name}')
    cols[1].image(COIN_TRANSLATION_TABLE[ticker]['link'], caption=None, width=64, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    cols[1].markdown(f'### ${ticker}')
    # current price
    current_price = dfs_history[ticker].tail(1)['price'][0]
    #current_price = round(current_price,8)
    current_price_str = '{:.8f}'.format(current_price)
    #current_price_str = str(current_price)
    cols[2].markdown(f'## €{current_price_str}')

    # percentage change
    prediction_price_to_show = predictions[ticker][23]
    percentage_change = ranking[ticker]
    prediction_price_to_show_str = '{:.8f}'.format(prediction_price_to_show)
    cols[3].metric(" ",f'€{prediction_price_to_show_str}', f'{round(percentage_change,2)}%')
    # chart
    # color for the prediction-line
    if prediction_price_to_show >= current_price:
        pred_color = 'green'
    else:
        pred_color = 'firebrick'

    fig = generate_price_line_chart(dfs_full[ticker].index,
                                    dfs_full[ticker]['price'],
                                    len(dfs_full[ticker])-24,
                                    coin_name=coin_name,
                                    pred_color=pred_color)
    cols[4].plotly_chart(fig #use_container_width=True
                         )
    st.markdown("""---""")
