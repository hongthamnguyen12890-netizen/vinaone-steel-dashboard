import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="VinaOne Steel", layout="wide")

st.title("📊 VinaOne Steel Dashboard")
st.subheader("HRC • Zinc • Margin Performance")

col1, col2, col3, col4 = st.columns(4)
col1.metric("HRC Price (USD/mt)", "510", "+12")
col2.metric("Zinc LME (USD/t)", "3,240", "+4")
col3.metric("Margin %", "18.5%", "-1.2%")
col4.metric("Completion Rate", "67%", "+3%")

# Donut chart
status = pd.DataFrame({'Status': ['Completed', 'Pending', 'Cancelled'], 'Count': [6705, 2300, 994]})
st.plotly_chart(px.pie(status, names='Status', values='Count', hole=0.4, title="Procurement Order by Status"), use_container_width=True)

# Bar chart
shipping = pd.DataFrame({'Source': ['Ấn Độ', 'CSVC Phú Mỹ', 'Trung Quốc'], 'Count': [3200, 1800, 4000]})
st.plotly_chart(px.bar(shipping, x='Source', y='Count', title="Order by Supply Source"), use_container_width=True)

# Line + Bar
monthly = pd.DataFrame({
    'Month': ['Oct 2023','Jan 2024','Apr 2024','Jul 2024'],
    'HRC Price': [480,520,510,530],
    'Revenue': [2.1,2.4,2.3,2.5]
})
fig = px.line(monthly, x='Month', y='HRC Price', title="HRC Price & Revenue by Month")
fig.add_bar(x=monthly['Month'], y=monthly['Revenue'], name='Revenue')
st.plotly_chart(fig, use_container_width=True)

st.caption("Dashboard VinaOne Steel - Tự động update")
