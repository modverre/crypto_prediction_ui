import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pytrends.request import TrendReq

pytrend = TrendReq()

#Page title
st.set_page_config(page_title="Crypto Predicto",
       page_icon="🤑",
       layout="wide",
    )
#Header
st.header("🤑CRYPTO PREDICTO🤑")

#Coin selection bar
clist = ['Dogecoin', 'Dogelon Mars', 'Samoyedcoin', 'Hoge Finance','Shiba Inu' ]
currency = st.selectbox("Select a coin:", clist)

#Sidebar
add_selectbox = st.sidebar.title(currency)
image = st.sidebar.image("/Users/nat.walentynowicz/Downloads/image.png", width=250)
marketcap = st.sidebar.markdown("**Market Capitalization:**")
age = st.sidebar.markdown("**How old is the coin:**")
overall_sen = st.sidebar.markdown("**Overall Sentiment:**")

#Colums
col1, col2 = st.columns(2)

#Colum1
prediction_index = col1.metric(label="Increase in the next 24h", value="+4.87%", delta="$46,583.91",)

#Colum2 - Price data
col2.subheader("Price data")
def get_line_chart_data():

    return pd.DataFrame(
            np.random.randn(20, 1),
            columns=[currency]
        )

df = get_line_chart_data()

col2.line_chart(df)

#Colum2 - Google Trends
col2.subheader("Google Trends")
pytrend.build_payload(kw_list=[currency])

# Interest by Region
df = pytrend.interest_over_time()

fig = px.line(df.reset_index(), x='date', y=currency)  #px.line(df[df['country'] == currency], x = "year", y = "gdpPercap",title = "GDP per Capita")
col2.plotly_chart(fig, use_container_width=True)

#col2.subheader("A narrow column with the data")
#col2.table(df.sort_values(by=currency, ascending=False))
