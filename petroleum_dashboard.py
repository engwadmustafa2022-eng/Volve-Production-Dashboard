import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Config
st.set_page_config(page_title="Volve Field Analytics", layout="wide")
st.title("🛢️ Volve Field Production Dashboard")

# 2. Function to find the Excel file automatically
def find_excel():
    for file in os.listdir('.'):
        if 'Volve' in file and file.endswith('.xlsx'):
            return file
    return None

# 3. Data Loading
file_name = find_excel()

if file_name:
    @st.cache_data
    def load_data(path):
        data = pd.read_excel(path)
        # Clean column names (remove spaces)
        data.columns = data.columns.str.strip()
        data['DATEPRD'] = pd.to_datetime(data['DATEPRD'])
        return data

    df = load_data(file_name)

    # 4. Sidebar Well Selection
    well_list = df['NPD_WELL_BORE_NAME'].unique()
    selected_well = st.sidebar.selectbox("Select Wellbore", well_list)

    # 5. Filtering
    filtered_df = df[df['NPD_WELL_BORE_NAME'] == selected_well]

    # 6. Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Oil (bbl)", f"{filtered_df['BORE_OIL_VOL'].sum():,.0f}")
    col2.metric("Avg Pressure", f"{filtered_df['AVG_DOWNHOLE_PRESSURE'].mean():.2f}")
    col3.metric("Max Temp", f"{filtered_df['AVG_DOWNHOLE_TEMPERATURE'].max():.2f}")

    # 7. Chart
    st.subheader(f"Production Performance: {selected_well}")
    fig = px.line(filtered_df, x='DATEPRD', y='BORE_OIL_VOL', title="Oil Production Rate")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ Excel file not found! Please make sure 'Volve production data.xlsx' is in the D:\mid-proj folder.")