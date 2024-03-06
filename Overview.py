import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
data = pd.read_csv("MIDAS_VN_Qdata_1Q2015_vF.csv")
st.set_page_config(layout = 'wide', page_title='Product Analyst')
st.header('MAIN MARKET | OVERVIEW')

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
sum_sale = data1[cot_sale].sum()
round_sum_list = list(data1[cot_sale].sum())
round_sum_list = [round(number) for number in round_sum_list]
round_sum_list= ['{:,.0f}'.format(number) for number in round_sum_list]
round_sum_list = [formatted_number.replace(',', '.') for formatted_number in round_sum_list]
qtr_nam = [f'{i}_Q{k}' for i in range(2012, 2015) for k in range(1, 5)]
sum_sale.index = qtr_nam
for i in range(4,len(sum_sale.values)):
  growth.append(round(((sum_sale.values[i]/sum_sale.values[i-4])-1)*100,1))

dates = qtr_nam[4:]
costs = list(sum_sale[4:])
scores = growth

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add bar chart to the primary y-axis
fig.add_trace(go.Bar(x=dates, y=costs, name='Cost'), secondary_y=False)

# Add line chart to the secondary y-axis
fig.add_trace(go.Scatter(x=dates, y=scores, name='Score'), secondary_y=True)

# Set the titles of the x-axis and y-axes
fig.update_layout(
    title_text="Overview",
    xaxis_title="Dates",
    yaxis_title="Main Market",
    yaxis2_title="Growth",
)

sum_sale = pd.DataFrame({'Main Market':sum_sale })
sum_sale  = sum_sale.reset_index().rename(columns={'index': don_vi})
growth = ["{:.1f}%".format(value) for value in growth]
sum_sale['Growth%']=  [' ']*4 + growth
sum_sale['Main Market'] = round_sum_list
sum_sale= sum_sale.T
sum_sale.columns = sum_sale.iloc[0]
sum_sale = sum_sale[1:]

# Show the figure
st.plotly_chart(fig)
st.dataframe(sum_sale)
if value == "UN'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Overview_UN.PNG')
elif value == "CU'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Overview_CU.PNG')
elif value == "VND'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Overview_VND.PNG')
elif value == "USD'000":
  st.subheader('Analyze data with Excel Microsoft')
  st.image('image/Overview_USD.PNG')
