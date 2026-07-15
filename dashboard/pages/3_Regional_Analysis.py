import streamlit as st
import pandas as pd
import plotly.express as px
import os
st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Regional Analysis")
st.markdown("Analyze sales and profit performance across regions and states.")

# ----------------------------
# Load Dataset
# ----------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "Enhanced_Superstore.csv"
)

df = pd.read_csv(DATA_PATH)

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

state = st.sidebar.multiselect(
    "State",
    options=sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["State"].isin(state))
]
st.sidebar.markdown("---")

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
# ----------------------------
# KPI Cards
# ----------------------------

k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
k2.metric("📈 Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
k3.metric("🗺️ States Selected", filtered_df["State"].nunique())

st.markdown("---")

# ----------------------------
# Top 10 States by Sales
# ----------------------------

st.subheader("🏆 Top 10 States by Sales")

top_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
    .reset_index()
)

fig = px.bar(
    top_sales,
    x="Sales",
    y="State",
    orientation="h",
    text_auto=True,
    color="Sales"
)

st.plotly_chart(fig,  width='stretch')
best_state = top_sales.iloc[-1]

st.info(
    f"💡 **Insight:** "
    f"**{best_state['State']}** recorded the highest sales "
    f"(${best_state['Sales']:,.0f})."
)

# ----------------------------
# Top 10 States by Profit
# ----------------------------

st.subheader("💰 Top 10 States by Profit")

top_profit = (
    filtered_df.groupby("State")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
    .reset_index()
)

fig = px.bar(
    top_profit,
    x="Profit",
    y="State",
    orientation="h",
    text_auto=True,
    color="Profit"
)

st.plotly_chart(fig,  width='stretch')
best_profit = top_profit.iloc[-1]

st.info(
    f"💡 **Insight:** "
    f"**{best_profit['State']}** generated the highest profit "
    f"(${best_profit['Profit']:,.0f})."
)

# ----------------------------
# Profit by Region
# ----------------------------

st.subheader("🌎 Profit by Region")

region_profit = (
    filtered_df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    text_auto=True,
    color="Region"
)

st.plotly_chart(fig, width='stretch')
top_region = region_profit.loc[region_profit["Profit"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{top_region['Region']}** is the most profitable region "
    f"with ${top_region['Profit']:,.0f} profit."
)