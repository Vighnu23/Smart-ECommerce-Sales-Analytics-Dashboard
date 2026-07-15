import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(
    page_title="Sales Forecasting",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Forecasting using Machine Learning")
st.markdown(
    """
This page uses a **Linear Regression Machine Learning model**
to predict the next **6 months of sales** based on historical
monthly sales data.
"""
)

# Load Dataset
df = pd.read_csv(
    "E:/ECommerce_Sales_Analysis/dataset/Enhanced_Superstore.csv"
)

# Convert Order Date to datetime
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    format="%d-%m-%Y"
)

# Monthly Sales
monthly_sales = (
    df.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

# Create Month Index
monthly_sales["Month_Number"] = range(len(monthly_sales))
# Features and Target
X = monthly_sales[["Month_Number"]]
y = monthly_sales["Sales"]

# Train Model
model = LinearRegression()
model.fit(X, y)
# Future Month Numbers
future_months = np.arange(
    len(monthly_sales),
    len(monthly_sales) + 6
).reshape(-1, 1)

# Predict Sales
predictions = model.predict(future_months)
# Last Date
last_date = monthly_sales["Order Date"].max()

# Next 6 Months
future_dates = pd.date_range(
    start=last_date + pd.offsets.MonthEnd(1),
    periods=6,
    freq="ME"
)
forecast_df = pd.DataFrame({
    "Order Date": future_dates,
    "Predicted Sales": predictions
})

# Actual Sales Data
actual_df = monthly_sales[["Order Date", "Sales"]].copy()
actual_df["Type"] = "Actual"

# Forecast Data
forecast_chart = forecast_df.rename(
    columns={"Predicted Sales": "Sales"}
)
forecast_chart["Type"] = "Forecast"

# Combine Data
combined_df = pd.concat(
    [actual_df, forecast_chart],
    ignore_index=True
)

# Forecast Chart
st.subheader("Actual Sales vs Forecasted Sales (Next 6 Months)")

fig = px.line(
    combined_df,
    x="Order Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Sales Forecast for the Next 6 Months"
)

st.plotly_chart(fig, use_container_width=True)
growth = (
    (predictions[-1] - predictions[0])
    / predictions[0]
) * 100
st.subheader("📋 Next 6 Months Sales Forecast")

forecast_df["Forecast Month"] = (
    forecast_df["Order Date"]
    .dt.strftime("%b %Y")
)

forecast_display = forecast_df[
    ["Forecast Month", "Predicted Sales"]
].copy()

forecast_display["Predicted Sales"] = (
    forecast_display["Predicted Sales"]
    .apply(lambda x: f"${x:,.0f}")
)

st.dataframe(
    forecast_display,
    use_container_width=True,
    hide_index=True
)
st.subheader("📊 Forecast Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Highest Predicted Sales",
        f"${forecast_df['Predicted Sales'].max():,.0f}"
    )

with col2:
    st.metric(
        "Average Predicted Sales",
        f"${forecast_df['Predicted Sales'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Lowest Predicted Sales",
        f"${forecast_df['Predicted Sales'].min():,.0f}"
    )
st.markdown("### 💡 Machine Learning Insight")

if growth > 0:
    st.success(
        f"""
The Linear Regression model predicts an overall
sales growth of **{growth:.1f}%**
over the next six months.

This indicates a positive sales trend.
"""
    )
else:
    st.warning(
        f"""
The model predicts a sales decline of
**{abs(growth):.1f}%**
over the next six months.

Business strategies may be needed to improve sales.
"""
    )
st.subheader("📌 Business Recommendations")

st.info(
    """
✅ Maintain sufficient inventory based on the forecasted demand.

✅ Increase marketing efforts during months with higher predicted sales.

✅ Focus on high-performing product categories to maximize revenue.

✅ Continuously monitor sales trends and retrain the forecasting model
with new data for improved accuracy.
"""
)