import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Smart E-Commerce Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart E-Commerce Sales Analytics Dashboard")
df = pd.read_csv("../dataset/Enhanced_Superstore.csv")

st.markdown(
    """
Welcome to the **Smart E-Commerce Sales Analytics Dashboard**.

This interactive dashboard provides valuable business insights from an
e-commerce sales dataset using **Python, Streamlit, Pandas, and Plotly**.

Use the **sidebar** to navigate through the different analysis pages.
"""
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Dashboard Pages")

    st.markdown("""
- 📊 **Overview**
  - Business KPIs
  - Sales by Category
  - Profit by Region
  - Sales by Segment
  - Payment Mode Distribution

- 📦 **Product Analysis**
  - Sales by Sub-Category
  - Profit by Sub-Category
  - Quantity by Category
""")

with col2:
    st.subheader("📈 More Analysis")

    st.markdown("""
- 🌍 **Regional Analysis**
  - Top 10 States by Sales
  - Top 10 States by Profit
  - Profit by Region

- 🚚 **Order & Trend Analysis**
  - Delivery Status
  - Ship Mode Analysis
  - Festival Season Orders
  - Monthly Sales Trend
  - Yearly Sales Trend
""")

st.markdown("---")

st.success("👈 Use the sidebar on the left to explore the dashboard.")
st.markdown("---")

st.subheader("📁 Dataset Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "📄 Total Records",
    len(df)
)

col2.metric(
    "📊 Total Columns",
    len(df.columns)
)

col3.metric(
    "🌍 Regions",
    df["Region"].nunique()
)

col4.metric(
    "📦 Categories",
    df["Category"].nunique()
)

st.info(
    """
### 🛠 Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
"""
)

st.markdown("---")

st.caption(
    "Developed by **Andhavarapu Vighna Priya** | "
    "B.Tech CSD | Internship Project"
)