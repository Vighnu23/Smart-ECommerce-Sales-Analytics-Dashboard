import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Order & Trend Analysis",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Order & Trend Analysis")
st.markdown("Analyze order performance and sales trends over time.")

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("../dataset/Enhanced_Superstore.csv")
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)
# Create Year-Month column
df["YearMonth"] = df["Order Date"].dt.to_period("M").astype(str)

# ----------------------------
# Sidebar Filters
# ----------------------------

st.sidebar.header("🔍 Filters")

ship_mode = st.sidebar.multiselect(
    "Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

festival = st.sidebar.multiselect(
    "Festival Season",
    options=df["Festival Season"].unique(),
    default=df["Festival Season"].unique()
)

filtered_df = df[
    (df["Ship Mode"].isin(ship_mode)) &
    (df["Festival Season"].isin(festival))
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

k1.metric("📦 Orders", len(filtered_df))
k2.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
k3.metric("🚚 Delivered", (filtered_df["Delivery Status"] == "Delivered").sum())

st.markdown("---")

# ----------------------------
# Delivery Status + Festival Season
# ----------------------------

left, right = st.columns(2)

with left:

    st.subheader("🚚 Order Delivery Status")

    delivery = (
        filtered_df["Delivery Status"]
        .value_counts()
        .reset_index()
    )

    delivery.columns = ["Status", "Count"]

    fig = px.pie(
        delivery,
        names="Status",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, width='stretch')
    top_delivery = delivery.loc[delivery["Count"].idxmax()]

    st.info(
       f"💡 **Insight:** "
       f"Most orders are **{top_delivery['Status']}**, "
       f"showing efficient order processing."
    )

with right:

    st.subheader("🎉 Orders by Festival Season")

    festival_orders = (
        filtered_df["Festival Season"]
        .value_counts()
        .reset_index()
    )

    festival_orders.columns = ["Festival", "Orders"]

    fig = px.pie(
        festival_orders,
        names="Festival",
        values="Orders",
        hole=0.4
    )

    st.plotly_chart(fig,  width='stretch')
    top_festival = festival_orders.loc[festival_orders["Orders"].idxmax()]

    st.info(
       f"💡 **Insight:** "
       f"Most orders were placed during **{top_festival['Festival']}**."
    )

# ----------------------------
# Ship Mode
# ----------------------------

st.subheader("🚢 Sales by Ship Mode")

ship_sales = (
    filtered_df.groupby("Ship Mode")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    ship_sales,
    x="Ship Mode",
    y="Sales",
    color="Ship Mode",
    text_auto=True
)

st.plotly_chart(fig,  width='stretch')
best_ship = ship_sales.loc[ship_sales["Sales"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{best_ship['Ship Mode']}** generated the highest sales."
)

# ----------------------------
# Monthly Sales Trend
# ----------------------------

st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df.groupby("YearMonth")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x="YearMonth",
    y="Sales",
    markers=True
)

st.plotly_chart(fig,  width='stretch')
best_month = monthly_sales.loc[monthly_sales["Sales"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"Highest sales were recorded in **{best_month['YearMonth']}**."
)

# ----------------------------
# Yearly Sales Trend
# ----------------------------

st.subheader("📊 Yearly Sales Trend")

yearly_sales = (
    filtered_df.groupby(filtered_df["Order Date"].dt.year)["Sales"]
    .sum()
    .reset_index()
)

yearly_sales.columns = ["Year", "Sales"]

fig = px.bar(
    yearly_sales,
    x="Year",
    y="Sales",
    text_auto=True,
    color="Year"
)

st.plotly_chart(fig,  width='stretch')
best_year = yearly_sales.loc[yearly_sales["Sales"].idxmax()]

st.info(
    f"💡 **Insight:** "
    f"**{int(best_year['Year'])}** achieved the highest annual sales."
)