import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
data = pd.read_csv(r"C:/Users/khanh/Documents/Market Analyst/MIDAS_VN_Qdata_1Q2015_vF.csv")
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('MAIN MARKET | CHANNEL')

value = st.selectbox(label = 'Chọn đơn vị', options = ["UN'000", "CU'000", "VND'000", "USD'000"])
don_vi = value

current_date_string = "31/3/2012"
cot_sale = []
growth = []
for i in range(12):
  if "UN" in don_vi:
    current_date_object = datetime.strptime(current_date_string, "%d/%m/%Y") + timedelta(90*i)
    cot_sale.append(f'UN\nQTR/{current_date_object.month}/{str(current_date_object.year)[-2:]}\n (Thousands)')
  if "CU" in don_vi:
    current_date_object = datetime.strptime(current_date_string, "%d/%m/%Y") + timedelta(90*i)
    cot_sale.append(f'CU\nQTR/{current_date_object.month}/{str(current_date_object.year)[-2:]}\n (Thousands)')
  if "VND" in don_vi:
    current_date_object = datetime.strptime(current_date_string, "%d/%m/%Y") + timedelta(90*i)
    cot_sale.append(f'LC/TRD\nQTR/{current_date_object.month}/{str(current_date_object.year)[-2:]}\n (Thousands)')
  if "USD" in don_vi:
    current_date_object = datetime.strptime(current_date_string, "%d/%m/%Y") + timedelta(90*i)
    cot_sale.append(f'USD/TRD\nQTR/{current_date_object.month}/{str(current_date_object.year)[-2:]}\n (Thousands)')
data1 = data[data['ATC3']=='C7A   B-BLOCKING AGENTS,PLAIN']
qtr_nam = [f'{i}_Q{k}' for i in range(2012, 2015) for k in range(1, 5)]
sum_channel = data1.groupby('CHANNEL')[cot_sale].sum()
sum_channel.columns = qtr_nam
sum_channel.index.name = don_vi
sum_channel.rename(index={'VIETNAM HOSPITAL': 'HOSPITAL', 'VIETNAM RETAIL': 'RETAIL'}, inplace=True)
sum_main = sum_channel[qtr_nam].sum()
sum_channel.loc['Main Market'] = list(sum_main)
hospital_share = [(sum_channel[i]['HOSPITAL'] / sum_channel[i]['Main Market']) * 100 for i in qtr_nam]
retail_share = [(sum_channel[i]['RETAIL'] / sum_channel[i]['Main Market']) * 100 for i in qtr_nam]
main_share = [x + y for x, y in zip(hospital_share, retail_share)]
market_share = pd.DataFrame({'Share%': qtr_nam , 'HOSPITAL': hospital_share, 'RETAIL': retail_share, 'Main Market': main_share})
market_share = market_share.T
market_share.columns = market_share.iloc[0]
market_share = market_share[1:]
market_share.iloc[:2, :] = market_share.iloc[:2, :].round(2)
market_share.index.name = "Share%"
growth_hospital = [((sum_channel[sum_channel.columns[i]]['HOSPITAL'] / sum_channel[sum_channel.columns[i-4]]['HOSPITAL']) - 1) * 100 for i in range(4, len(sum_channel.columns))]
growth_retail = [((sum_channel[sum_channel.columns[i]]['RETAIL'] / sum_channel[sum_channel.columns[i-4]]['RETAIL']) - 1) * 100 for i in range(4, len(sum_channel.columns))]
growth_main = [((sum_channel[sum_channel.columns[i]]['Main Market'] / sum_channel[sum_channel.columns[i-4]]['Main Market']) - 1) * 100 for i in range(4, len(sum_channel.columns))]

Growth = pd.DataFrame({'Growth%': qtr_nam , 'HOSPITAL': [' ']*4 + growth_hospital, 'RETAIL': [' ']*4 + growth_retail, 'Main Market': [' ']*4 + growth_main})
Growth = Growth.T
Growth.columns = Growth.iloc[0]
Growth = Growth[1:]
Growth.iloc[:, -8:] = (Growth.iloc[:,4:].round().applymap(lambda x: f'{x:.1f}%')).values
Growth.index.name = "Growth%"
trace1 = go.Scatter(
                    x = sum_channel.columns,
                    y = list(sum_channel.loc['HOSPITAL']),
                    mode = "lines+markers",
                    name = "HOSPITAL",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text= sum_channel.columns)
trace2 = go.Scatter(
                    x = sum_channel.columns,
                    y = list(sum_channel.loc['RETAIL']),
                    mode = "lines+markers",
                    name = "RETAIL",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text= sum_channel.columns)
layout = go.Layout(title=don_vi)

# Create figure
figure = go.Figure(data=[trace1, trace2], layout=layout)
#Vis_MS
trace1_MS = go.Scatter(
                    x = market_share.columns,
                    y = list(market_share.loc['HOSPITAL']),
                    mode = "lines+markers",
                    name = "HOSPITAL",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text= market_share.columns)
trace2_MS = go.Scatter(
                    x = market_share.columns,
                    y = list(market_share.loc['RETAIL']),
                    mode = "lines+markers",
                    name = "RETAIL",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text= market_share.columns)
layout_MS = go.Layout(title="MS%")

# Create figure
figure_MS = go.Figure(data=[trace1_MS, trace2_MS], layout=layout_MS)

# Display the plot
#figure_MS.show()
market_share = market_share.round().applymap(lambda x: f'{x:.1f}%')
sum_channel= sum_channel.round().applymap(lambda x: f'{x:,.0f}').replace(',', '.', regex=True)

column1 , column2 = st.columns((2))
with column1:
  st.plotly_chart(figure, use_container_width= True)
with column2:
  st.plotly_chart(figure_MS, use_container_width= True)
st.dataframe(sum_channel)
st.dataframe(market_share)
st.dataframe(Growth)

if value == "UN'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Channel_UN.PNG')
elif value == "CU'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Channel_CU.PNG')
elif value == "VND'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Channel_VND.PNG')
elif value == "USD'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Channel_USD.PNG')
