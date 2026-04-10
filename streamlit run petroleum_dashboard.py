import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="Petroleum Production Analytics", layout="wide")
st.title("🛢️ Volve Field Production Analytics Dashboard")
st.markdown("---")

# 
@st.cache_data
def load_data():
    data = pd.read_csv("final_clean_data.csv")
    data['DATEPRD'] = pd.to_datetime(data['DATEPRD'])
    return data

df = load_data()

# Sidebar - 
well_selection = st.sidebar.selectbox(
    "Select Target Wellbore", 
    df['NPD_WELL_BORE_NAME'].unique()
)

# 
filtered_df = df[df['NPD_WELL_BORE_NAME'] == well_selection]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Cumulative Oil (bbl)", f"{filtered_df['BORE_OIL_VOL'].sum():,.0f}")
col2.metric("Avg Downhole Pressure (psi)", f"{filtered_df['AVG_DOWNHOLE_PRESSURE'].mean():.2f}")
col3.metric("Well Count", len(df['NPD_WELL_BORE_NAME'].unique()))

# 
st.subheader(f"Detailed Analysis for Well: {well_selection}")
fig = px.area(filtered_df, x='DATEPRD', y='BORE_OIL_VOL', 
              title="Production Decline Curve")
st.plotly_chart(fig, use_container_width=True)