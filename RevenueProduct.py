import pandas as pd
import re
from datetime import datetime, timedelta
from functools import reduce
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import numpy as np
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('DAILY REVENUE PRODUCT')

start_date = datetime(2014, 1, 1)
end_date = datetime(2014, 12, 31)
selected_date = st.slider('Chọn ngày:', start_date, end_date, (start_date, end_date))
input_date =  pd.to_datetime(selected_date[1])
data_13 = pd.read_csv('Sales Data 2013.csv')
data_13 = data_13.drop(['BRAND'], axis = 1)
pattern = r'^(\S+)(?:\s+\S+(?:\s+\S+)*)?' # xài RE để lấy kí tự cần lấy
brand_13 = [re.findall(pattern, item)[0] for item in data_13['Item Description']]
data_13['BRAND'] = brand_13 # ghép cột Brand sau khi xử lý
invoice_date_13 = list(data_13['Invoice Confirmed Date'])
invoice_date_13 = [datetime.strptime(str(date), '%Y%m%d').strftime('%d/%m/%Y') for date in invoice_date_13]
data_13['Invoice Date'] = invoice_date_13
data_13['Invoice Date'] = pd.to_datetime(data_13['Invoice Date'], format='%d/%m/%Y') # định dạng từ str sang kiểu datatime
data_13 = data_13[['BRAND','Invoice Date','Net Sales Value']] # lấy những bảng cần lấy để xử lý
data_14 = pd.read_csv('/content/drive/MyDrive/Data/Sales Data 2014.csv')
data_14 = data_14.drop(['Brand','Region'], axis = 1)
invoice_date = list(data_14['Invoice Confirmed Date'])
invoice_date = [datetime.strptime(str(date), '%Y%m%d').strftime('%d/%m/%Y') for date in invoice_date ]
data_14['Invoice Date'] = invoice_date
data_14['Invoice Date'] = pd.to_datetime(data_14['Invoice Date'], format='%d/%m/%Y')
pattern = r'^(\S+)(?:\s+\S+(?:\s+\S+)*)?'
brand_14 = [re.findall(pattern, item)[0] for item in data_14['Item Description']]
data_14['BRAND'] = brand_14
data_14 = data_14[['BRAND','Invoice Date','Net Sales Value']]

# Lọc MTD trong data lớn
MTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month == input_date.month) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'].dt.day <= input_date.day)] # lọc MTD theo data lớn
MTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month == input_date.month) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'].dt.day <= input_date.day)]
SumMTD_14 = MTD_14.groupby('BRAND')['Net Sales Value'].sum()
data_MTD_14 = SumMTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
SumMTD_13 = MTD_13.groupby('BRAND')['Net Sales Value'].sum()
data_MTD_13 = SumMTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
merge_MTD = pd.merge(data_MTD_14, data_MTD_13 , on=['BRAND'], how='outer')
merge_MTD  = merge_MTD.sort_values(by ='This Year Sales', ascending = False).reset_index(drop=True)
merge_MTD = merge_MTD.fillna(0)

growth_MTD = []
for i in range(len(merge_MTD)):
  growth_MTD.append(((merge_MTD['This Year Sales'][i]/merge_MTD['Last Year Sales'][i])-1)*100)
merge_MTD['Growth'] = growth_MTD
for i in range(len(merge_MTD['Growth'])):
    if merge_MTD['Growth'][i] == float('inf'):
        merge_MTD['Growth'][i] = 150

# Lọc QTD trong data lớn
if 1 <= input_date.month and input_date.month <= 3:
  QTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month >= 1) & (data_14['Invoice Date'].dt.month <= 3) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_14 = MTD_14.groupby('BRAND')['Net Sales Value'].sum()
  QTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month >= 1) & (data_13['Invoice Date'].dt.month <= 3) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_13 = MTD_13.groupby('BRAND')['Net Sales Value'].sum()
  data_QTD_14 = SumQTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
  data_QTD_13 = SumQTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
if 4 <= input_date.month and input_date.month <= 6:
  QTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month >= 4) & (data_14['Invoice Date'].dt.month <= 6) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_14 = MTD_14.groupby('BRAND')['Net Sales Value'].sum()
  QTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month >= 4) & (data_13['Invoice Date'].dt.month <= 6) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_13 = MTD_13.groupby(['ZP Item Code','BRAND'])['Net Sales Value'].sum()
  data_QTD_14 = SumQTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
  data_QTD_13 = SumQTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
if 7 <= input_date.month and input_date.month <= 9:
  QTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month >= 7) & (data_14['Invoice Date'].dt.month <= 9) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_14 = MTD_14.groupby('BRAND')['Net Sales Value'].sum()
  QTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month >= 7) & (data_13['Invoice Date'].dt.month <= 9) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_13 = MTD_13.groupby('BRAND')['Net Sales Value'].sum()
  data_QTD_14 = SumQTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
  data_QTD_13 = SumQTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
if 10 <= input_date.month and input_date.month <= 12:
  QTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month >= 10) & (data_14['Invoice Date'].dt.month <= 12) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_14 = MTD_14.groupby(['BRAND'])['Net Sales Value'].sum()
  QTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month >= 10) & (data_13['Invoice Date'].dt.month <= 12) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
  SumQTD_13 = MTD_13.groupby(['BRAND'])['Net Sales Value'].sum()
  data_QTD_14 = SumQTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
  data_QTD_13 = SumQTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
merge_QTD = pd.merge(data_QTD_14, data_QTD_13 , on=['BRAND'], how='outer')
merge_QTD  = merge_QTD.sort_values(by ='This Year Sales', ascending = False).reset_index(drop=True)
merge_QTD = merge_QTD.fillna(0)
growth_QTD = []
for i in range(len(merge_QTD)):
  growth_QTD.append(((merge_QTD['This Year Sales'][i]/merge_QTD['Last Year Sales'][i])-1)*100)
merge_QTD['Growth'] = growth_QTD
for i in range(len(merge_QTD['Growth'])):
    if merge_QTD['Growth'][i] == float('inf'):
        merge_QTD['Growth'][i] = 150


# lọc YTD theo data lớn
YTD_14 = data_14.loc[(data_14['Invoice Date'].dt.month >= 1) & (data_14['Invoice Date'].dt.month <= input_date.month) & (data_14['Invoice Date'].dt.day >= 1) & (data_14['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]
YTD_13 = data_13.loc[(data_13['Invoice Date'].dt.month >= 1) & (data_13['Invoice Date'].dt.month <= input_date.month) & (data_13['Invoice Date'].dt.day >= 1) & (data_13['Invoice Date'] <= pd.Timestamp(f"{input_date.year}-{input_date.month}-{input_date.day} 00:00:00"))]

SumYTD_14 = YTD_14.groupby('BRAND')['Net Sales Value'].sum()
data_YTD_14 = SumYTD_14.reset_index(name='This Year Sales')[['BRAND','This Year Sales']]
SumYTD_13 = YTD_13.groupby('BRAND')['Net Sales Value'].sum()
data_YTD_13 = SumYTD_13.reset_index(name='Last Year Sales')[['BRAND','Last Year Sales']]
merge_YTD = pd.merge(data_YTD_14, data_YTD_13 , on=['BRAND'], how='outer')
merge_YTD  = merge_YTD.sort_values(by ='This Year Sales', ascending = False).reset_index(drop=True)
merge_YTD = merge_YTD.fillna(0)
growth_YTD = []
for i in range(len(merge_YTD)):
  growth_YTD.append(((merge_YTD['This Year Sales'][i]/merge_YTD['Last Year Sales'][i])-1)*100)
merge_YTD['Growth'] = growth_YTD
for i in range(len(merge_YTD['Growth'])):
    if merge_YTD['Growth'][i] == float('inf'):
        merge_YTD['Growth'][i] = 150
# data_report_1 =  pd.concat([merge_MTD, merge_QTD, merge_YTD], axis=1).head(10)

data_report_1 = pd.merge(pd.merge(merge_MTD, merge_QTD, on=['BRAND']), merge_YTD, on=['BRAND'])
data_report_1.columns = ['BRAND','This Year Sales_MTD','Last Year Sales_MTD','Growth_MTD',
                        'This Year Sales_QTD','Last Year Sales_QTD','Growth_QTD','This Year Sales_YTD','Last Year Sales_YTD','Growth_YTD']
round_sales = ['This Year Sales_MTD','Last Year Sales_MTD','This Year Sales_QTD',
              'Last Year Sales_QTD','This Year Sales_YTD','Last Year Sales_YTD']
data_visual_1 = data_report_1.sort_values(by ='This Year Sales_YTD', ascending = False).reset_index(drop=True).head(10)
data_visual_1[round_sales] = data_visual_1[round_sales].astype(int)
data_report_1[['Growth_MTD','Growth_QTD','Growth_YTD']] = data_report_1[['Growth_MTD','Growth_QTD','Growth_YTD']].applymap(lambda x: f'{x:.1f}%')

data_report_1 = data_report_1.sort_values(by ='This Year Sales_YTD', ascending = False).reset_index(drop=True)
data_report_1[round_sales] = data_report_1[round_sales].applymap(lambda x: f'{x:,.0f}').replace(',', '.', regex=True)
data_report_1 = data_report_1.head(10)


fig_MTD = go.Figure()

# Thêm cột cho This Year Sales_MTD và Last Year Sales_MTD
fig_MTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['This Year Sales_MTD'], name='This Year Sales_MTD'))
fig_MTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['Last Year Sales_MTD'], name='Last Year Sales_MTD'))

# Thêm đường line cho Growth_MTD
fig_MTD.add_trace(go.Scatter(x=data_visual_1['BRAND'], y=data_visual_1['Growth_MTD'], mode='lines+markers', name='Growth_MTD', yaxis='y2'))

# Cấu hình trục y phụ cho đường line
fig_MTD.update_layout(
    yaxis2=dict(
        title='Growth_MTD',
        overlaying='y',
        side='right'
    ),
    title='Sales MTD',
    barmode='group'
)




fig_QTD = go.Figure()

# Thêm cột cho This Year Sales_MTD và Last Year Sales_MTD
fig_QTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['This Year Sales_QTD'], name='This Year Sales_QTD'))
fig_QTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['Last Year Sales_QTD'], name='Last Year Sales_QTD'))

# Thêm đường line cho Growth_MTD
fig_QTD.add_trace(go.Scatter(x=data_visual_1['BRAND'], y=data_visual_1['Growth_QTD'], mode='lines+markers', name='Growth_QTD', yaxis='y2'))

# Cấu hình trục y phụ cho đường line
fig_QTD.update_layout(
    yaxis2=dict(
        title='Growth_QTD',
        overlaying='y',
        side='right'
    ),
    title='Sales QTD',
    barmode='group'
)





fig_YTD = go.Figure()

# Thêm cột cho This Year Sales_MTD và Last Year Sales_MTD
fig_YTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['This Year Sales_YTD'], name='This Year Sales_YTD'))
fig_YTD.add_trace(go.Bar(x=data_visual_1['BRAND'], y=data_visual_1['Last Year Sales_YTD'], name='Last Year Sales_YTD'))

# Thêm đường line cho Growth_MTD
fig_YTD.add_trace(go.Scatter(x=data_visual_1['BRAND'], y=data_visual_1['Growth_YTD'], mode='lines+markers', name='Growth_=YTD', yaxis='y2'))

# Cấu hình trục y phụ cho đường line
fig_YTD.update_layout(
    yaxis2=dict(
        title='Growth_YTD',
        overlaying='y',
        side='right'
    ),
    title='Sales YTD',
    barmode='group'
)


column1 , column2 , column3 = st.columns((3))
with column1:
  st.plotly_chart(fig_MTD, use_container_width= True)
with column2:
  st.plotly_chart(fig_QTD, use_container_width= True)
with column3:
  st.plotly_chart(fig_YTD, use_container_width= True)
st.dataframe(data_report_1,hide_index =True)
