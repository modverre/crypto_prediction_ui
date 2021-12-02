import requests
import streamlit as st
import pandas as pd
import numpy as np
from params import COIN_TRANSLATION_TABLE
import datetime as datetime
from plotly import graph_objs as go
import plotly.express as px
import plotly.io as pio

st.set_page_config(page_title='test', page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)
st.markdown('<style>body{background-color: #234;}</style>',unsafe_allow_html=True)

#import streamlit.components.v1 as components
#components.iframe("https://xdisplays.net/priv/test.html")

HtmlFile = open("test.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
#print(source_code)
#components.html(source_code)

st.markdown(source_code, unsafe_allow_html= True)
st.markdown('ahahahah')
