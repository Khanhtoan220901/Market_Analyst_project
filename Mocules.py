import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
data = pd.read_csv(r"C:/Users/khanh/Documents/Market Analyst/MIDAS_VN_Qdata_1Q2015_vF.csv")
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('MAIN MARKET | MOCULES')

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
data_pro = (data1.groupby('PRODUCT')[cot_sale].sum()).sum(axis=1) # tính tổng các product của tất cả các năm
data_pro = data_pro.sort_values(ascending=False)
data_pro =  data1['PRODUCT'].isin(list(data_pro.head(5).index)) #  chọn ra 5 product có sale cao nhất
filtered_df = data1[data_pro]
data_kq_pro = filtered_df.groupby('PRODUCT')[cot_sale].sum()
data_kq_pro.columns = qtr_nam # reset header theo định dạng
data_kq_pro.index.name = don_vi # reset tên cột index
data_main_pro = data1[cot_sale].sum() # tính tổng market main
sum_pro = data_kq_pro[qtr_nam].sum() # tính tổng 5 product đầu
other_product = [x - y for x, y in zip(list(data_main_pro), list(sum_pro))] # tính cột other = Main - sum(5 cái đầu)
data_kq_pro.loc['OTHER'] = pd.Series(other_product, index=data_kq_pro.columns) # thêm hàng Other vào bảng
data_kq_pro.loc['Main Market'] = pd.Series(list(data_main_pro), index=data_kq_pro.columns)# thêm hàng Main vào bảng
# tính market share
data_share = []
for i in qtr_nam:
  data_share.append([(data_kq_pro[i][data_kq_pro.index[0]]/ data_kq_pro[i]['Main Market'])* 100,(data_kq_pro[i][data_kq_pro.index[1]]/ data_kq_pro[i]['Main Market'])* 100,(data_kq_pro[i][data_kq_pro.index[2]]/ data_kq_pro[i]['Main Market'])* 100,(data_kq_pro[i][data_kq_pro.index[3]]/ data_kq_pro[i]['Main Market'])* 100,(data_kq_pro[i][data_kq_pro.index[4]]/ data_kq_pro[i]['Main Market'])* 100])
data_kq_share =pd.DataFrame(data_share,columns=list(data_kq_pro.index[:-2]))
share_other = []
for i in qtr_nam:
  share_other.append((data_kq_pro[i]['OTHER']/ data_kq_pro[i]['Main Market'])* 100)
data_kq_share = data_kq_share.T
data_kq_share.columns = qtr_nam
data_kq_share.index.name = "Share%"
data_kq_share.loc['OTHER'] = pd.Series(share_other, index=data_kq_share.columns)
data_main_sum = data_kq_share[qtr_nam].sum()
data_kq_share.loc['Main Market'] = pd.Series(list(data_main_sum), index=data_kq_share.columns)
# tính tăng trưởng
data_growth = []
share_growth = []
for i in range(4, len(data_kq_pro.columns)):
  data_growth.append([((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[0]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[0]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[1]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[1]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[2]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[2]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[3]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[3]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[4]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[4]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[5]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[5]])-1)* 100,
  ((data_kq_pro[data_kq_pro.columns[i]][data_kq_pro.index[6]]/ data_kq_pro[data_kq_pro.columns[i-4]][data_kq_pro.index[6]])-1)* 100])
data_kq_growth =pd.DataFrame(data_growth,columns=list(data_kq_pro.index))
data_kq_growth = data_kq_growth.T
data_kq_growth.columns = qtr_nam[4:12]
data_kq_growth[qtr_nam[0:4]] = ' '
data_kq_growth = data_kq_growth[qtr_nam]
data_kq_growth.index.name = "Growth%"
data_pro_vis = []
for i in list(data_kq_pro.index[:-2]):
  data_pro_vis.append(go.Scatter(
                    x = data_kq_pro.columns,
                    y = list(data_kq_pro.loc[i]),
                    mode = "lines+markers",
                    name = i,
                    text= data_kq_pro.columns))
layout = go.Layout(title=don_vi,yaxis=dict(rangemode='tozero'))

# Create figure
figure = go.Figure(data=data_pro_vis, layout=layout)


data_share_vis = []
for i in list(data_kq_share.index[:-2]):
  data_share_vis.append(go.Scatter(
                    x = data_kq_share.columns,
                    y = list(data_kq_share.loc[i]),
                    mode = "lines+markers",
                    name = i,
                    text= data_kq_share.columns))
layout_share = go.Layout(title="MS%",yaxis=dict(rangemode='tozero'))

# Create figure
figure_share = go.Figure(data=data_share_vis, layout=layout_share)
data_kq_growth.iloc[:, -8:] = data_kq_growth.iloc[:,4:].round(1).astype(str) + '%'
data_kq_pro= data_kq_pro.round().applymap(lambda x: f'{x:,.0f}').replace(',', '.', regex=True)
data_kq_share = data_kq_share.round().applymap(lambda x: f'{x:.1f}%')
column1 , column2 = st.columns((2))
with column1:
  st.plotly_chart(figure, use_container_width= True)
with column2:
  st.plotly_chart(figure_share, use_container_width= True)
st.dataframe(data_kq_pro)
st.dataframe(data_kq_share)
st.dataframe(data_kq_growth)
if value == "UN'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Molecules_UN.PNG')
elif value == "CU'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Molecules_CU.PNG')
elif value == "VND'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Molecules_VND.PNG')
elif value == "USD'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image(r'C:/Users/khanh/Documents/Market Analyst/image/Molecules_USD.PNG')
