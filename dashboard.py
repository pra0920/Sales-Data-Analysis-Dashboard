import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Page settings
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ===== PROFESSIONAL DASHBOARD STYLE =====

st.markdown("""
<style>
/* Main dashboard background */
.stApp {
    background-color: #F4F7FB !important;
}

/* Content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Main title */
h1 {
    color: #17365D !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
}

/* Section headings */
h2, h3 {
    color: #24476B !important;
    font-weight: 700 !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF !important;
    padding: 20px !important;
    border-radius: 14px !important;
    border: 1px solid #E2E8F0 !important;
    box-shadow: 0 3px 10px rgba(23, 54, 93, 0.06);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 600 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #17365D !important;
    font-weight: 750 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #EAF0F8 !important;
}

/* Charts and other bordered containers */
[data-testid="stPlotlyChart"],
[data-testid="stAltairChart"] {
    background-color: #FFFFFF;
    border-radius: 14px;
    padding: 10px;
}

/* Buttons */
.stButton > button {
    background-color: #17365D;
    color: #FFFFFF;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #24476B;
    color: #FFFFFF;
    border: none;
}
</style>
""", unsafe_allow_html=True)


st.title("Sales Data Analysis Dashboard")
st.write("Explore sales performance using interactive filters.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("sales_large.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["TotalSales"] = df["Quantity"] * df["UnitPrice"]
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "sales_large.csv was not found. "
        "Keep it in the same folder as dashboard.py."
    )
    st.stop()

    # --- Data Quality Checks ---
st.subheader("🛡️ Data Quality Checks")

missing_values = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())
negative_sales = int((df["TotalSales"] < 0).sum())

col1, col2, col3 = st.columns(3)

col1.metric("Missing Values", missing_values)
col2.metric("Duplicate Rows", duplicate_rows)
col3.metric("Negative Sales Values", negative_sales)

if missing_values == 0 and duplicate_rows == 0 and negative_sales == 0:
    st.success("No basic data-quality issues detected!")
else:
    st.warning("Please review the data-quality issues above.")

# Sidebar filters
st.sidebar.header("Dashboard Filters")


products = st.sidebar.multiselect(
    "Choose products",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

regions = st.sidebar.multiselect(
    "Choose regions",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

# Date Range Filter
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply all dashboard filters

if isinstance(date_range, tuple):
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = max_date
else:
    start_date = date_range
    end_date = date_range

filtered_df = df[
    df["Product"].isin(products)
    & df["Region"].isin(regions)
    & (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
].copy()


if filtered_df.empty:
    st.warning("No sales match these filters.")
    st.stop()


# KPI calculations
total_revenue = filtered_df["TotalSales"].sum()

total_orders = filtered_df["OrderID"].nunique()

units_sold = filtered_df["Quantity"].sum()

average_order = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

st.subheader("Sales Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Units Sold", f"{units_sold:,}")
col4.metric("Avg. Order Revenue", f"₹{average_order:,.0f}")

# Sales Summary

st.subheader("📋 Sales Summary")

st.write(
    f"Your selected data contains **{total_orders:,} orders** "
    f"and **{units_sold:,} units sold**, generating total revenue "
    f"of **₹{total_revenue:,.2f}**."
)


if total_orders > 0:
    st.write(
        f"The average revenue per order is "
        f"**₹{average_order:,.2f}**."
    )
else:
    st.info("No sales data available for the selected filters.")


# Prepare charts
filtered_df["Month"] = (
    filtered_df["Date"].dt.to_period("M").astype(str)
)

monthly_sales = (
    filtered_df.groupby("Month")["TotalSales"]
    .sum()
    .sort_index()
)

product_sales = (
    filtered_df.groupby("Product")["TotalSales"]
    .sum()
    .sort_values()
)

region_sales = (
    filtered_df.groupby("Region")["TotalSales"]
    .sum()
    .sort_values()
)


# Interactive Monthly Revenue Trend
st.subheader("📈 Monthly Revenue Trend")

monthly_chart_data = monthly_sales.reset_index()
monthly_chart_data.columns = ["Month", "Revenue"]

fig_monthly = px.line(
    monthly_chart_data,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Performance",
    template="plotly_white"
)

fig_monthly.update_traces(
    line=dict(width=3),
    marker=dict(size=9),
    hovertemplate="Month: %{x}<br>Revenue: ₹%{y:,.2f}<extra></extra>"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue (₹)",
    hovermode="x unified"
)

st.plotly_chart(fig_monthly, use_container_width=True)


# Product and region charts
left, right = st.columns(2)

    
with left:
    st.subheader("🛍️ Revenue by Product")

    product_chart_data = product_sales.reset_index()
    product_chart_data.columns = ["Product", "Revenue"]

    fig_product = px.bar(
        product_chart_data,
        x="Revenue",
        y="Product",
        orientation="h",
        title="Product-wise Revenue",
        color="Revenue",
        template="plotly_white"
    )

    fig_product.update_layout(
        xaxis_title="Revenue (₹)",
        yaxis_title="Product",
        showlegend=False
    )

    st.plotly_chart(fig_product, use_container_width=True)

    
with right:
    st.subheader("🌍 Revenue by Region")

    region_chart_data = region_sales.reset_index()
    region_chart_data.columns = ["Region", "Revenue"]

    fig_region = px.bar(
        region_chart_data,
        x="Region",
        y="Revenue",
        title="Region-wise Revenue",
        color="Revenue",
        template="plotly_white"
    )

    fig_region.update_layout(
        xaxis_title="Region",
        yaxis_title="Revenue (₹)",
        showlegend=False
    )

    st.plotly_chart(fig_region, use_container_width=True)



# ===== PRODUCT PERFORMANCE ANALYTICS =====

st.subheader("🏆 Product Performance Analytics")

product_analysis = (
    filtered_df.groupby("Product")
    .agg(
        Total_Revenue=("TotalSales", "sum"),
        Units_Sold=("Quantity", "sum"),
        Total_Orders=("OrderID", "nunique"),
        Average_Price=("UnitPrice", "mean")
    )
    .reset_index()
)

# Calculate revenue contribution
product_analysis["Revenue_Share_%"] = (
    product_analysis["Total_Revenue"]
    / product_analysis["Total_Revenue"].sum()
    * 100
)

# Sort products by revenue
product_analysis = product_analysis.sort_values(
    "Total_Revenue",
    ascending=False
)

# Display top 5 products
st.write("### Top 5 Products by Revenue")

top_products = product_analysis.head(5)

st.dataframe(
    top_products,
    use_container_width=True,
    hide_index=True
)

# Interactive product chart
fig_top_products = px.bar(
    top_products,
    x="Total_Revenue",
    y="Product",
    orientation="h",
    color="Revenue_Share_%",
    title="Top 5 Products by Revenue",
    template="plotly_white",
    hover_data=["Units_Sold", "Total_Orders"]
)

fig_top_products.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Total Revenue (₹)",
    yaxis_title="Product"
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True
)

# Top-Selling Product

top_selling_product = product_analysis.loc[
    product_analysis["Units_Sold"].idxmax()
]

st.info(
    f"🏆 Top-selling product: **{top_selling_product['Product']}** "
    f"with **{top_selling_product['Units_Sold']:,} units sold**."
)


# ===== AUTOMATED BUSINESS INSIGHTS =====

st.subheader("🧠 Automated Business Insights")

# Product generating highest revenue
best_product = product_analysis.iloc[0]

# Region generating highest revenue
region_analysis = (
    filtered_df.groupby("Region")
    .agg(
        Revenue=("TotalSales", "sum"),
        Units_Sold=("Quantity", "sum"),
        Orders=("OrderID", "nunique")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

best_region = region_analysis.iloc[0]

# Best performing month
best_month = monthly_sales.idxmax()
best_month_revenue = monthly_sales.max()

# Product revenue contribution
top_product_share = best_product["Revenue_Share_%"]

# Display insights
col1, col2 = st.columns(2)

with col1:
    st.info(
        f"🏆 **Top Product:** {best_product['Product']} "
        f"generated ₹{best_product['Total_Revenue']:,.2f} "
        f"in revenue."
    )

    st.success(
        f"🌍 **Top Region:** {best_region['Region']} "
        f"generated ₹{best_region['Revenue']:,.2f} "
        f"in revenue."
    )

with col2:
    st.info(
        f"📅 **Best Month:** {best_month} "
        f"recorded ₹{best_month_revenue:,.2f} "
        f"in revenue."
    )

    st.warning(
        f"📊 **Revenue Concentration:** "
        f"{top_product_share:.2f}% of total revenue "
        f"came from {best_product['Product']}."
    )




   # Sales Growth Analysis

st.header("📈 Sales Growth Analysis")

monthly_growth = (
    filtered_df
    .set_index("Date")
    .resample("MS")["TotalSales"]
    .sum()
    .reset_index()
)

monthly_growth["Growth_%"] = (
    monthly_growth["TotalSales"].pct_change() * 100
)

monthly_growth["Month"] = monthly_growth["Date"].dt.strftime("%b %Y")

# Monthly revenue and growth table
st.subheader("Monthly Revenue Growth")

st.dataframe(
    monthly_growth[
        ["Month", "TotalSales", "Growth_%"]
    ].round(2),
    use_container_width=True
)

# Growth chart
fig_growth = px.bar(
    monthly_growth.dropna(),
    x="Month",
    y="Growth_%",
    title="Month-over-Month Revenue Growth",
    text_auto=".2f"
)

st.plotly_chart(fig_growth, use_container_width=True)

# Best performing month
best_month = monthly_growth.loc[
    monthly_growth["TotalSales"].idxmax()
]

st.success(
    f"Your best-performing month was "
    f"{best_month['Month']} with revenue of "
    f"₹{best_month['TotalSales']:,.2f}."
)

# Download Monthly Sales Report

report_csv = monthly_growth[
    ["Month", "TotalSales", "Growth_%"]
].to_csv(index=False)

st.download_button(
    label="📥 Download Monthly Sales Report",
    data=report_csv,
    file_name="monthly_sales_report.csv",
    mime="text/csv"
)



# Data table

st.subheader("🔍 Explore the Sales Data")
st.caption("Use the filters above to explore the records included in this analysis.")

# Your existing data table code continues below


st.subheader("Sales Records")

st.dataframe(
    filtered_df.sort_values("Date"),
    use_container_width=True,
    hide_index=True
)

# Download filtered records
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv_data,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

st.caption(
    "Learning project using sample sales data. "
    "Figures are not actual company results."
)