import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
data = pd.read_csv("MIDAS_VN_Qdata_1Q2015_vF.csv")
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('MAIN MARKET | BRANDED_GX')

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
sum_channel = data1.groupby('BRANDS/GENERICS')[cot_sale].sum()
sum_channel.columns = qtr_nam
sum_channel.index.name = don_vi
sum_channel.rename(index={'BRANDS': 'BRANDED', 'GENERICS': 'GENERIC'}, inplace=True)
sum_main = sum_channel[qtr_nam].sum()
sum_channel.loc['Main Market'] = list(sum_main)
hospital_share = [(sum_channel[i]['BRANDED'] / sum_channel[i]['Main Market']) * 100 for i in qtr_nam]
retail_share = [(sum_channel[i]['GENERIC'] / sum_channel[i]['Main Market']) * 100 for i in qtr_nam]
main_share = [x + y for x, y in zip(hospital_share, retail_share)]
market_share = pd.DataFrame({'Share%': qtr_nam , 'BRANDED': hospital_share, 'GENERIC': retail_share, 'Main Market': main_share})
market_share = market_share.T
market_share.columns = market_share.iloc[0]
market_share = market_share[1:]
growth_hospital = [((sum_channel[sum_channel.columns[i]]['BRANDED'] / sum_channel[sum_channel.columns[i-4]]['BRANDED']) - 1) * 100 for i in range(4, len(sum_channel.columns))]
growth_retail = [((sum_channel[sum_channel.columns[i]]['GENERIC'] / sum_channel[sum_channel.columns[i-4]]['GENERIC']) - 1) * 100 for i in range(4, len(sum_channel.columns))]
growth_main = [((sum_channel[sum_channel.columns[i]]['Main Market'] / sum_channel[sum_channel.columns[i-4]]['Main Market']) - 1) * 100 for i in range(4, len(sum_channel.columns))]

Growth = pd.DataFrame({'Growth%': qtr_nam , 'BRANDED': [' ']*4 + growth_hospital, 'GENERIC': [' ']*4 + growth_retail, 'Main Market': [' ']*4 + growth_main})
Growth = Growth.T
Growth.columns = Growth.iloc[0]
Growth = Growth[1:]
Growth.iloc[:, -8:] = (Growth.iloc[:,4:].round().applymap(lambda x: f'{x:.1f}%')).values
Growth.index.name = "Growth%"

trace1 = go.Scatter(
                    x = sum_channel.columns,
                    y = list(sum_channel.loc['BRANDED']),
                    mode = "lines+markers",
                    name = "BRANDED",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text= sum_channel.columns)
trace2 = go.Scatter(
                    x = sum_channel.columns,
                    y = list(sum_channel.loc['GENERIC']),
                    mode = "lines+markers",
                    name = "GENERIC",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text= sum_channel.columns)
layout = go.Layout(title=don_vi,yaxis=dict(rangemode='tozero'))

# Create figure
figure = go.Figure(data=[trace1, trace2], layout=layout)
# Visual MS
trace1_MS = go.Scatter(
                    x = market_share.columns,
                    y = list(market_share.loc['BRANDED']),
                    mode = "lines+markers",
                    name = "BRANDED",
                    marker = dict(color = 'rgba(16, 112, 2, 0.8)'),
                    text= market_share.columns)
trace2_MS = go.Scatter(
                    x = market_share.columns,
                    y = list(market_share.loc['GENERIC']),
                    mode = "lines+markers",
                    name = "GENERIC",
                    marker = dict(color = 'rgba(80, 26, 80, 0.8)'),
                    text= market_share.columns)
layout_MS = go.Layout(title="MS%",
                  yaxis=dict(rangemode='tozero'))

# Create figure
figure_MS = go.Figure(data=[trace1_MS, trace2_MS], layout=layout_MS)
# Display the plot
market_share = market_share.round().applymap(lambda x: f'{x:.1f}%')
market_share.index.name = "Share%"
Growth.index.name = "Growth%"
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
  st.image('image/Branded_GX_UN.PNG')
elif value == "CU'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Branded_GX_CU.PNG')
elif value == "VND'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Branded_GX_VND.PNG')
elif value == "USD'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Branded_GX_USD.PNG')
