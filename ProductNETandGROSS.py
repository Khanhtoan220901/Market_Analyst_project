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
st.header('NET AND GROSS PRICING DETERMINE THE REVENUE FROM A PRODUCT')

months = range(1, 13)  # Tạo một list chứa các tháng từ 1 đến 12
data_months = ['aaa','January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
data_14 = pd.read_csv('Sales Data 2014.csv')
data_13 = pd.read_csv('Sales Data 2013.csv')
data_14 = data_14.drop(['Brand','Region'], axis = 1)
invoice_date = list(data_14['Invoice Confirmed Date'])
invoice_date = [datetime.strptime(str(date), '%Y%m%d').strftime('%d/%m/%Y') for date in invoice_date ]
data_14['Invoice Date'] = invoice_date
data_14['Invoice Date'] = pd.to_datetime(data_14['Invoice Date'], format='%d/%m/%Y')
pattern = r'^(\S+)(?:\s+\S+(?:\s+\S+)*)?'
brand_14 = [re.findall(pattern, item)[0] for item in data_14['Item Description']]
data_14['BRAND'] = brand_14
data_14_gross = data_14[['BRAND','Invoice Date','Selling Price','Net Qty']]
data_14 = data_14[['BRAND','Invoice Date','Net Sales Value']]


monthly_data_14 = {}

for month in months:
    # Lọc dữ liệu cho từng tháng
    monthly_data_14[f'month_{month}'] = data_14.loc[data_14['Invoice Date'].dt.month == month]

monthly_sum_14 = {}
for month in months:
  monthly_sum_14[f'month_{month}'] = monthly_data_14[f'month_{month}'].groupby(['BRAND'])['Net Sales Value'].sum()

data_sum_montly_14 = {}
for month in months:
    data_sum_montly_14[f'month_{month}'] = monthly_sum_14[f'month_{month}'].reset_index(name= data_months[month])[['BRAND',data_months[month]]]
data_sum_months_14 = [data_sum_montly_14['month_1'], data_sum_montly_14['month_2'],data_sum_montly_14['month_3'],data_sum_montly_14['month_4'],
                  data_sum_montly_14['month_5'],data_sum_montly_14['month_6'],data_sum_montly_14['month_7'],data_sum_montly_14['month_8'],
                  data_sum_montly_14['month_9'],data_sum_montly_14['month_10'],data_sum_montly_14['month_11'],data_sum_montly_14['month_12']]
result_data_14 = reduce(lambda left, right: pd.merge(left, right, on=['BRAND'], how = 'outer'), data_sum_months_14)
result_data_14 = result_data_14.fillna(0)
Input_brand = st.selectbox(label = 'Chọn Brand', options = list(result_data_14['BRAND']))

Name_sale_14 = result_data_14[result_data_14['BRAND'] == Input_brand].iloc[:, 1:]
Name_sale_14.insert(0, 'Monthly', 'This Year Sale (Net)')
gross_sale = []
for i in data_14_gross['Selling Price']:
  gross_sale.append(i * 0.1)
data_14_gross['Gross Sales'] = gross_sale
gross_sale_value = []
for i in range(len(data_14_gross)):
  gross_sale_value.append(data_14_gross['Gross Sales'][i] * data_14_gross['Net Qty'][i])
data_14_gross['Gross Sales Value'] =gross_sale_value
# data_14_gross = data_14_gross.round()
# data_14_gross['Gross Sales Value'] = data_14_gross['Gross Sales Value'].astype(int)
data_14_gross = data_14_gross.drop(['Selling Price', 'Net Qty','Gross Sales'], axis=1)

monthly_data_14_gross= {}

for month in months:
    # Lọc dữ liệu cho từng tháng
    monthly_data_14_gross[f'month_{month}'] = data_14_gross.loc[data_14_gross['Invoice Date'].dt.month == month]

monthly_sum_14_gross = {}
for month in months:
  monthly_sum_14_gross[f'month_{month}'] = monthly_data_14_gross[f'month_{month}'].groupby(['BRAND'])['Gross Sales Value'].sum()

sum_montly_14_gross = {}
for month in months:
    sum_montly_14_gross[f'month_{month}'] = monthly_sum_14_gross[f'month_{month}'].reset_index(name= data_months[month])[['BRAND',data_months[month]]]
sum_months_14_gross = [sum_montly_14_gross['month_1'], sum_montly_14_gross['month_2'],sum_montly_14_gross['month_3'],sum_montly_14_gross['month_4'],
                  sum_montly_14_gross['month_5'],sum_montly_14_gross['month_6'],sum_montly_14_gross['month_7'],sum_montly_14_gross['month_8'],
                  sum_montly_14_gross['month_9'],sum_montly_14_gross['month_10'],sum_montly_14_gross['month_11'],sum_montly_14_gross['month_12']]
result_data_14_gross = reduce(lambda left, right: pd.merge(left, right, on=['BRAND'], how = 'outer'), sum_months_14_gross)
result_data_14_gross = result_data_14_gross.fillna(0)
Name_sale_14_gross = result_data_14_gross[result_data_14_gross['BRAND'] == Input_brand].iloc[:, 1:]
Name_sale_14_gross.insert(0, 'Monthly', 'This Year Sale (Gross)')

data_13 = data_13.drop(['BRAND'], axis = 1)
pattern = r'^(\S+)(?:\s+\S+(?:\s+\S+)*)?' # xài RE để lấy kí tự cần lấy
brand_13 = [re.findall(pattern, item)[0] for item in data_13['Item Description']]
data_13['BRAND'] = brand_13 # ghép cột Brand sau khi xử lý
invoice_date_13 = list(data_13['Invoice Confirmed Date'])
invoice_date_13 = [datetime.strptime(str(date), '%Y%m%d').strftime('%d/%m/%Y') for date in invoice_date_13]
data_13['Invoice Date'] = invoice_date_13
data_13['Invoice Date'] = pd.to_datetime(data_13['Invoice Date'], format='%d/%m/%Y') # định dạng từ str sang kiểu datatime
data_13 = data_13[['BRAND','Invoice Date','Net Sales Value']]
# Tạo một dictionary để lưu trữ các DataFrame tương ứng với từng tháng
monthly_data_13 = {}

for month in months:
    # Lọc dữ liệu cho từng tháng
    monthly_data_13[f'month_{month}'] = data_13.loc[data_13['Invoice Date'].dt.month == month]

monthly_sum_13 = {}
for month in months:
  monthly_sum_13[f'month_{month}'] = monthly_data_13[f'month_{month}'].groupby(['BRAND'])['Net Sales Value'].sum()

data_sum_montly_13 = {}
for month in months:
    data_sum_montly_13[f'month_{month}'] = monthly_sum_13[f'month_{month}'].reset_index(name= data_months[month])[['BRAND',data_months[month]]]
data_sum_months_13 = [data_sum_montly_13['month_1'], data_sum_montly_13['month_2'],data_sum_montly_13['month_3'],data_sum_montly_13['month_4'],
                  data_sum_montly_13['month_5'],data_sum_montly_13['month_6'],data_sum_montly_13['month_7'],data_sum_montly_13['month_8'],
                  data_sum_montly_13['month_9'],data_sum_montly_13['month_10'],data_sum_montly_13['month_11'],data_sum_montly_13['month_12']]
result_data_13 = reduce(lambda left, right: pd.merge(left, right, on=['BRAND'], how = 'outer'), data_sum_months_13)
result_data_13 = result_data_13.fillna(0)
if Input_brand in list(result_data_13['BRAND']):
  Name_sale_13 = result_data_13[result_data_13['BRAND'] == Input_brand].iloc[:, 1:]
  Name_sale_13.insert(0, 'Monthly', 'Last Year Sale (Net)')
else:
  header = ['Monthly', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  row = ['Last Year Sale (Net)'] + [0] * 12
  Name_sale_13 = pd.DataFrame([row], columns=header)
data_report = pd.concat([Name_sale_13, Name_sale_14,Name_sale_14_gross], axis=0)
data_report.set_index('Monthly', inplace=True)
discount = [x/y if y != 0 else np.nan for x, y in zip(list(data_report.loc['This Year Sale (Net)']), list(data_report.loc['This Year Sale (Gross)']))]

def round_list(input_list, num_decimal_places=0): #hàm làm tròn 1 list
    rounded_list = []
    for item in input_list:
      if item == np.nan:
        rounded_list.append(np.nan)
      else:
        rounded_list.append(round(item, num_decimal_places))
    return rounded_list

discount = round_list(discount, 1)
data_report.loc['Discount'] = discount
Full_year = [sum(list(data_report.loc['Last Year Sale (Net)'])), sum(list(data_report.loc['This Year Sale (Net)'])),
          sum(list(data_report.loc['This Year Sale (Gross)'])), (sum(list(data_report.loc['This Year Sale (Net)']))/sum(list(data_report.loc['This Year Sale (Gross)'])))]
data_report['Full Year'] = Full_year
def convert_float_to_int(value):
    if np.isnan(value):
        return np.nan
    else:
        return int(value)
data_visual = data_report
data_visual = data_visual.applymap(convert_float_to_int)

fig = go.Figure()

# Thêm cột cho This Year Sales_MTD và Last Year Sales_MTD
fig.add_trace(go.Bar(x=list(data_visual.columns[:-1]), y=list(data_visual.loc['Last Year Sale (Net)'][:-1]), name='Last Year Sale (Net)'))
fig.add_trace(go.Bar(x=list(data_visual.columns[:-1]), y=list(data_visual.loc['This Year Sale (Net)'][:-1]), name='This Year Sale (Net)'))
fig.add_trace(go.Bar(x=list(data_visual.columns[:-1]), y=list(data_visual.loc['This Year Sale (Gross)'][:-1]), name='This Year Sale (Gross)'))
# Thêm đường line cho Growth_MTD
fig.add_trace(go.Scatter(x=list(data_visual.columns[:-1]), y=list(data_visual.loc['Discount'][:-1]), mode='lines+markers', name='Discount', yaxis='y2'))

# Cấu hình trục y phụ cho đường line
fig.update_layout(
    yaxis2=dict(
        title='Discount',
        overlaying='y',
        side='right'
    ),
    title='Sales Comparison Net and Gross',
    barmode='group'
)

data_report.iloc[0:3] = data_report.iloc[0:3].applymap(lambda x: f'{x:,.0f}').replace(',', '.', regex=True)
data_report.loc['Discount'] = data_report.loc['Discount'].apply(lambda x: f'{x:.1f}%' if not np.isnan(x) else x)
st.plotly_chart(fig)
st.dataframe(data_report)
