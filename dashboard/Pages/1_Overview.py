import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Overview Dashboard")
st.markdown("High-level overview of sales performance and business metrics.")

# Load Dataset
df = pd.read_csv("E:/ECommerce_Sales_Analysis/dataset/Enhanced_Superstore.csv")
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

segment = st.sidebar.multiselect(
    "Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment))
]
st.sidebar.markdown("---")

st.sidebar.download_button(
    label="📥 Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${filtered_df['Sales'].sum():,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"${filtered_df['Profit'].sum():,.0f}"
)

col3.metric(
    "📦 Total Orders",
    len(filtered_df)
)

col4.metric(
    "🏷️ Avg Discount",
    f"{filtered_df['Discount'].mean():.2f}"
)
left, right = st.columns(2)
with left:

    st.subheader("Sales by Category")

    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)

    top_category = category_sales.loc[category_sales["Sales"].idxmax()]

    st.info(
        f"💡 **Insight:** "
        f"{top_category['Category']}** generated the highest sales "
        f"(${top_category['Sales']:,.0f})."
    )
with right:

    st.subheader("Profit by Region")

    region_profit = (
        filtered_df.groupby("Region")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        text_auto=True
    )

    st.plotly_chart(fig, use_container_width=True)
    top_region = region_profit.loc[region_profit["Profit"].idxmax()]

    st.info(
         f"💡 **Insight:** "
         f"{top_region['Region']} region earned the highest profit "
         f"(${top_region['Profit']:,.0f})."
    )
left, right = st.columns(2)
with left:

    st.subheader("Sales by Segment")

    segment_sales = (
        filtered_df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
    top_segment = segment_sales.loc[segment_sales["Sales"].idxmax()]

    st.info(
            f"💡 **Insight:** "
            f"{top_segment['Segment']} segment contributed the highest sales."
      )
with right:

    st.subheader("Payment Mode Distribution")

    payment = (
        filtered_df["Payment Mode"]
        .value_counts()
        .reset_index()
    )

    payment.columns = ["Payment Mode", "Count"]

    fig = px.pie(
        payment,
        names="Payment Mode",
        values="Count",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)
    top_payment = payment.loc[payment["Count"].idxmax()]

    st.info(
        f"💡 **Insight:** "
        f"Most customers preferred **{top_payment['Payment Mode']}** "
        f"for payment."
    )
