import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="VinaOne Steel Dashboard", layout="wide", page_icon="📈")

# Sidebar filters (Slicer)
st.sidebar.title("Filters")
month = st.sidebar.selectbox("Month", ["All", "Sep 2026", "Aug 2026", "Jul 2026", "Jun 2026"])
year = st.sidebar.selectbox("Year", ["All", "2026", "2025"])
source = st.sidebar.multiselect("Supply Source", ["All", "Ấn Độ", "CSVC Phú Mỹ", "Trung Quốc", "Hàn Quốc"])
product = st.sidebar.selectbox("Product", ["All", "HRC", "Zinc", "Freight", "Margin"])

# Bookmarks (nút chuyển tab)
# Tabs (Bookmarks) - nút chuyển tab
tab_overview, tab_hrc_zinc, tab_margin_risk, tab_supply = st.tabs(["Overview", "HRC & Zinc", "Margin & Risk", "Supply Sources"])

# Tab 1: Overview (Dashboard chính)
with tab_overview:
    st.title("📊 VinaOne Steel Overview Dashboard")
    st.subheader("HRC • Zinc • Margin • Freight Performance (Sep 2023 - Sep 2026)")

    # KPI Cards với conditional formatting
    col1, col2, col3, col4 = st.columns(4)
    hrc_delta = data['HRC_Price'].pct_change().iloc[-1] * 100 if len(data) > 1 else 0
    zinc_delta = data['Zinc_Price'].pct_change().iloc[-1] * 100 if len(data) > 1 else 0
    margin_delta = data['Margin_%'].pct_change().iloc[-1] * 100 if len(data) > 1 else 0
    completion_delta = data['Completion_Rate_%'].pct_change().iloc[-1] * 100 if len(data) > 1 else 0

    col1.metric("HRC Price (USD/mt)", f"{data['HRC_Price'].iloc[-1]}", f"{hrc_delta:+.1f}%", delta_color="normal")
    col2.metric("Zinc LME (USD/t)", f"{data['Zinc_Price'].iloc[-1]}", f"{zinc_delta:+.1f}%", delta_color="normal")
    col3.metric("Margin %", f"{data['Margin_%'].iloc[-1]}%", f"{margin_delta:+.1f}%", delta_color="inverse" if margin_delta < 0 else "normal")
    col4.metric("Completion Rate %", f"{data['Completion_Rate_%'].iloc[-1]}%", f"{completion_delta:+.1f}%", delta_color="normal")

    # Donut chart - Procurement Order by Status (custom tooltip)
    status_data = pd.DataFrame({'Status': ['Completed', 'Pending', 'Cancelled'], 'Count': [6705, 2300, 994]})
    fig_donut = px.pie(status_data, names='Status', values='Count', hole=0.4, title="Procurement Order by Status")
    fig_donut.update_traces(hovertemplate="%{label}: %{value} orders<br>Percentage: %{percent:.1%}")
    st.plotly_chart(fig_donut, use_container_width=True)

    # Bar chart - Order by Supply Source
    shipping_data = pd.DataFrame({'Source': ['Ấn Độ', 'CSVC Phú Mỹ', 'Trung Quốc', 'Hàn Quốc'], 'Count': [3200, 1800, 4000, 900]})
    fig_bar = px.bar(shipping_data, x='Source', y='Count', title="Order by Supply Source", color='Source')
    fig_bar.update_traces(hovertemplate="Source: %{x}<br>Orders: %{y}")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line + Bar combo - HRC Price & Revenue by Month
    fig_combo = px.line(data, x='Month', y='HRC_Price', title="HRC Price & Revenue by Month", markers=True)
    fig_combo.add_bar(x=data['Month'], y=data['Revenue_M'], name='Revenue (M USD)', yaxis='y2')
    fig_combo.update_layout(yaxis2=dict(overlaying='y', side='right'))
    fig_combo.update_traces(hovertemplate="Month: %{x}<br>HRC: %{y:.0f} USD<br>Revenue: %{y2:.1f}M USD")
    st.plotly_chart(fig_combo, use_container_width=True)

    # Table Monthly performance với conditional formatting
    st.subheader("Monthly Performance Table")
    st.dataframe(data.style.format({
        'HRC_Price': '{:.0f}',
        'Zinc_Price': '{:,.0f}',
        'Margin_%': '{:.1f}%',
        'Completion_Rate_%': '{:.0f}%',
        'Revenue_M': '{:.2f}M'
    }).background_gradient(subset=['Margin_%'], cmap='RdYlGn'), use_container_width=True)

# Tab 2: HRC & Zinc Deep Dive
with tab_hrc_zinc:
    st.header("HRC & Zinc Deep Dive")
    st.line_chart(data.set_index('Month')[['HRC_Price', 'Zinc_Price']])

# Tab 3: Margin & Risk Analysis
with tab_margin_risk:
    st.header("Margin & Risk Analysis")
    st.bar_chart(data.set_index('Month')['Margin_%'])

# Tab 4: Supply Sources & CBPG Alert
with tab_supply:
    st.header("Supply Sources & CBPG Alert")
    st.write("CBPG Trung Quốc: 19–27.83% (vẫn hiệu lực 5 năm)")
    st.bar_chart(shipping_data.set_index('Source')['Count'])

    # KPI Cards với conditional formatting
    col1, col2, col3, col4 = st.columns(4)
    hrc_delta = data['HRC_Price'].pct_change().iloc[-1] * 100
    zinc_delta = data['Zinc_Price'].pct_change().iloc[-1] * 100
    margin_delta = data['Margin_%'].pct_change().iloc[-1] * 100
    completion_delta = data['Completion_Rate_%'].pct_change().iloc[-1] * 100

    col1.metric("HRC Price (USD/mt)", f"{data['HRC_Price'].iloc[-1]}", f"{hrc_delta:+.1f}%", delta_color="normal")
    col2.metric("Zinc LME (USD/t)", f"{data['Zinc_Price'].iloc[-1]}", f"{zinc_delta:+.1f}%", delta_color="normal")
    col3.metric("Margin %", f"{data['Margin_%'].iloc[-1]}%", f"{margin_delta:+.1f}%", delta_color="inverse" if margin_delta < 0 else "normal")
    col4.metric("Completion Rate %", f"{data['Completion_Rate_%'].iloc[-1]}%", f"{completion_delta:+.1f}%", delta_color="normal")

    # Donut chart - Order by Status (custom tooltip)
    status_data = pd.DataFrame({'Status': ['Completed', 'Pending', 'Cancelled'], 'Count': [6705, 2300, 994]})
    fig_donut = px.pie(status_data, names='Status', values='Count', hole=0.4, title="Procurement Order by Status")
    fig_donut.update_traces(hovertemplate="%{label}: %{value} orders<br>Percentage: %{percent:.1%}")
    st.plotly_chart(fig_donut, use_container_width=True)

    # Bar chart - Order by Supply Source
    shipping_data = pd.DataFrame({'Source': ['Ấn Độ', 'CSVC Phú Mỹ', 'Trung Quốc', 'Hàn Quốc'], 'Count': [3200, 1800, 4000, 900]})
    fig_bar = px.bar(shipping_data, x='Source', y='Count', title="Order by Supply Source", color='Source')
    fig_bar.update_traces(hovertemplate="Source: %{x}<br>Orders: %{y}")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Line + Bar combo - HRC Price & Revenue by Month
    fig_combo = px.line(data, x='Month', y='HRC_Price', title="HRC Price & Revenue by Month", markers=True)
    fig_combo.add_bar(x=data['Month'], y=data['Revenue_M'], name='Revenue (M USD)', yaxis='y2')
    fig_combo.update_layout(yaxis2=dict(overlaying='y', side='right'))
    fig_combo.update_traces(hovertemplate="Month: %{x}<br>HRC: %{y:.0f} USD<br>Revenue: %{y2:.1f}M USD")
    st.plotly_chart(fig_combo, use_container_width=True)

    # Table Monthly performance với conditional formatting
    st.subheader("Monthly Performance Table")
    st.dataframe(data.style.format({
        'HRC_Price': '{:.0f}',
        'Zinc_Price': '{:,.0f}',
        'Margin_%': '{:.1f}%',
        'Completion_Rate_%': '{:.0f}%',
        'Revenue_M': '{:.2f}M'
    }).background_gradient(subset=['Margin_%'], cmap='RdYlGn'), use_container_width=True)

# Tab 2: HRC & Zinc
with tabs[1]:
    st.header("HRC & Zinc Deep Dive")
    st.line_chart(data.set_index('Month')[['HRC_Price', 'Zinc_Price']])

# Tab 3: Margin & Risk
with tabs[2]:
    st.header("Margin & Risk Analysis")
    st.bar_chart(data.set_index('Month')['Margin_%'])

# Tab 4: Supply Sources
with tabs[3]:
    st.header("Supply Sources & CBPG Alert")
    st.write("CBPG Trung Quốc: 19–27.83% (vẫn hiệu lực 5 năm)")
    st.bar_chart(shipping_data.set_index('Source')['Count'])

st.caption("Dashboard VinaOne Steel - Tự động update từ dữ liệu nội bộ. Liên hệ em để kết nối Google Sheet/ERP.")
