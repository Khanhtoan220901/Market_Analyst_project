
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
data = pd.read_csv("MIDAS_VN_Qdata_1Q2015_vF.csv")
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('TOP 20 CORPORATIONS IN TOTAl PHARMA MARKET')

sale_name = [i for i in list(data.columns)if "14" in i and "LC" in i ]
sale_name_truoc = [i for i in list(data.columns)if "13" in i and "LC" in i ]
data_kq_14 = (data.groupby('CORPORATION')[sale_name].sum()).sum(axis=1)
data_kq_14 = data_kq_14.reset_index(name='Total_14')[['CORPORATION', 'Total_14']]
data_kq_14 = pd.DataFrame(data_kq_14)
data_kq_13 = (data.groupby('CORPORATION')[sale_name_truoc].sum()).sum(axis=1)
data_kq_13 = data_kq_13.reset_index(name='Total_13')[['CORPORATION', 'Total_13']]
data_kq_13 = pd.DataFrame(data_kq_13)
growth = []
for i in range(len(data_kq_14)):
  growth.append(((data_kq_14['Total_14'][i]/data_kq_13['Total_13'][i])-1)*100)
Market_share = []
for i in data_kq_14['Total_14']:
  Market_share.append((i/sum(data_kq_14['Total_14'])*100))
Total_growth = ((sum(data_kq_14['Total_14'])/sum(data_kq_13['Total_13'])-1)*100)
EI = []
for i in growth:
  EI.append((1+(i/100))/(1+(Total_growth/100))*100)
data_top = {
    'CORPORATION': list(data_kq_14['CORPORATION']),
    'FY-2014': list(data_kq_14['Total_14']),
    'Growth': growth,
    'MS%' : Market_share,
    'Evol Index' : EI
}
data_top = pd.DataFrame(data_top)
data_top_20  = (data_top.sort_values(by ='FY-2014', ascending = False)).reset_index(drop=True)
new_range_index = pd.RangeIndex(start=1, stop=len(data_top_20)+1, step=1)
data_top_20.index = new_range_index
My_Cop = data_top_20[data_top_20['CORPORATION']=='MENARINI']
data_top_20 = data_top_20.head(20)
data_top_20 = data_top_20.append(My_Cop)
data_index = list(data_top_20.index)
data_top_20.insert(0, 'Rank FY-2014', data_index)

sale_name_future = [i for i in list(data.columns)if "3/15" in i and "LC" in i ]
sale_name_truoc_future = [i for i in list(data.columns)if "3/14" in i and "LC" in i ]
data_kq_15 = (data.groupby('CORPORATION')[sale_name_future].sum()).sum(axis=1)
data_kq_15 = data_kq_15.reset_index(name='Total_15')[['CORPORATION', 'Total_15']]
data_kq_15 = pd.DataFrame(data_kq_15)
data_kq_14_1 = (data.groupby('CORPORATION')[sale_name_truoc_future].sum()).sum(axis=1)
data_kq_14_1 = data_kq_14_1.reset_index(name='Total_14')[['CORPORATION', 'Total_14']]
data_kq_14_1 = pd.DataFrame(data_kq_14_1)
growth_future = []
for i in range(len(data_kq_15)):
  growth_future.append(((data_kq_15['Total_15'][i]/data_kq_14_1['Total_14'][i])-1)*100)
Market_share_future = []
for i in data_kq_15['Total_15']:
  Market_share_future.append((i/sum(data_kq_15['Total_15'])*100))
Total_growth_future = ((sum(data_kq_15['Total_15'])/sum(data_kq_14_1['Total_14'])-1)*100)
EI_future = []
for i in growth_future:
  EI_future.append((1+(i/100))/(1+(Total_growth_future/100))*100)
data_top_future = {
    'CORPORATION': list(data_kq_15['CORPORATION']),
    'FY-2015': list(data_kq_15['Total_15']),
    'Growth': growth_future,
    'MS%' : Market_share_future,
    'Evol Index' : EI_future
}
data_top_future = pd.DataFrame(data_top_future)
data_top_20_future  = (data_top_future.sort_values(by ='FY-2015', ascending = False)).reset_index(drop=True)
new_range_index = pd.RangeIndex(start=1, stop=len(data_top_20_future)+1, step=1)
data_top_20_future.index = new_range_index
data_index = list(data_top_20_future.index)
data_top_20_future.insert(0, 'Rank FY-2015', data_index)
data_report_20 = pd.merge(data_top_20, data_top_20_future, on='CORPORATION',how= 'left')
data_report_20 =  data_report_20[list(data_report_20.columns)].rename(columns={'Growth_x': 'Growth_2014', 'MS%_x': 'MS%_2014', 'Evol Index_x':'Evol Index_2014',
                                                                              'Growth_y' :'Growth_2015', 'MS%_y': 'MS%_2015', 'Evol Index_y': 'Evol Index_2015'})
data_report_20[['FY-2014','FY-2015']] = data_report_20[['FY-2014','FY-2015']].round().applymap(lambda x: f'{x:,.0f}').replace(',', '.', regex=True)
data_report_20[['Growth_2014','Growth_2015','MS%_2014','Evol Index_2014','Evol Index_2015','MS%_2015']] = data_report_20[['Growth_2014','Growth_2015','MS%_2014','Evol Index_2014','Evol Index_2015','MS%_2015']].round(1)
def color_gradient(val):

    if "🡅" in val:
        color = 'green'
    elif "🡇" in val :
        color = 'red'
    else:
        color = 'black'
    return f'color: {color}'

def add_icon(val):
    if (val - data_report_20[data_report_20["Rank FY-2015"] == val]['Rank FY-2014']).values > 0:
        return f'{val} 🡇'  # Icon cho điểm cao
    elif (val - data_report_20[data_report_20["Rank FY-2015"] == val]['Rank FY-2014']).values < 0:
        return f'{val} 🡅'  # Icon cho điểm trung bình
    else:
        return f'{val}'  # Icon cho điểm thấp
def color_down(val):
  if val < 0 : 
    color = 'red'
  else: 
    color = 'blue'
  return f'color: {color}' 

data_report_20['Rank FY-2015'] = data_report_20['Rank FY-2015'].apply(add_icon)
data_report_20 = data_report_20.style.applymap(color_gradient, subset=['Rank FY-2015'])
data_report_20 = data_report_20.applymap(color_down, subset=['Growth_2014','Growth_2015'])
columns_to_format = ['Growth_2014', 'Growth_2015', 'MS%_2014', 'Evol Index_2014', 'Evol Index_2015', 'MS%_2015']
data_report_20 = data_report_20.format({'Growth_2014': '{:.1f}%', 'Growth_2015': '{:.1f}%', 'MS%_2014': '{:.1f}%', 'Evol Index_2014': '{:.1f}%', 'Evol Index_2015': '{:.1f}%', 'MS%_2015': '{:.1f}%'})
data_report_20 = data_report_20.hide_index()
headers = {
    'selector': 'th.col_heading',
    'props': 'background-color: #000066; color: white;'
}
data_report_20  = data_report_20.set_table_styles([headers])
html_styled_df = data_report_20.render()

# Hiển thị DataFrame đã được định dạng trên Streamlit
st.write(html_styled_df, unsafe_allow_html=True)
st.subheader('Analyze data with Excel Microsoft')
st.image('image/Top20 Corporation.PNG')
