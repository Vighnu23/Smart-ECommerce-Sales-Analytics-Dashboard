import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
st.set_page_config(
    page_title="Product Analysis",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Analysis")
st.markdown("Analyze product performance based on Sales, Profit and Quantity.")

# Load Dataset
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "dataset" / "Enhanced_Superstore.csv"

df = pd.read_csv(DATA_PATH)
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

# Sidebar Filters
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

sub_category = st.sidebar.multiselect(
    "Sub Category",
    df["Sub-Category"].unique(),
    default=df["Sub-Category"].unique()
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Sub-Category"].isin(sub_category))
]
st.sidebar.markdown("---")

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# -----------------------------

st.subheader("📈 Sales by Sub Category")

sales_sub = (
    filtered_df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig = px.bar(
    sales_sub,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    text_auto=True,
    color="Sales"
)

st.plotly_chart(fig, width='stretch')
top_sub = sales_sub.loc[sales_sub["Sales"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{top_sub['Sub-Category']}** generated the highest sales "
    f"(${top_sub['Sales']:,.0f})."
)

# -----------------------------

st.subheader("💰 Profit by Sub Category")

profit_sub = (
    filtered_df.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig = px.bar(
    profit_sub,
    x="Profit",
    y="Sub-Category",
    orientation="h",
    text_auto=True,
    color="Profit"
)

st.plotly_chart(fig,  width='stretch')
top_profit_sub = profit_sub.loc[profit_sub["Profit"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{top_profit_sub['Sub-Category']}** generated the highest profit "
    f"(${top_profit_sub['Profit']:,.0f})."
)

# -----------------------------

st.subheader("📦 Quantity by Category")

qty = (
    filtered_df.groupby("Category")["Quantity"]
    .sum()
    .reset_index()
)

fig = px.bar(
    qty,
    x="Category",
    y="Quantity",
    text_auto=True,
    color="Category"
)

st.plotly_chart(fig, width='stretch')
top_qty = qty.loc[qty["Quantity"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{top_qty['Category']}** recorded the highest quantity sold "
    f"({top_qty['Quantity']:,} units)."
)
