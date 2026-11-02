import pandas as pd

# Load our sales dataset
df = pd.read_csv("sales_large.csv")

# Calculate revenue for each order
df["TotalSales"] = df["Quantity"] * df["UnitPrice"]

# Monthly Sales Analysis

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.to_period("M")

monthly_sales = df.groupby("Month")["TotalSales"].sum()

print("\n===== MONTHLY SALES =====")
print(monthly_sales)

print("\nMonth with Highest Revenue:")
print(monthly_sales.idxmax())

# 1. Display the dataset
print("\n===== SALES DATA ANALYSIS =====")
print(df.to_string(index=False))

# 2. Calculate total revenue
print("\n===== TOTAL REVENUE =====")
print("Total Revenue:", df["TotalSales"].sum())

# 3. Find revenue by product
print("\n===== SALES BY PRODUCT =====")
product_sales = df.groupby("Product")["TotalSales"].sum()
print(product_sales.sort_values(ascending=False))

# 4. Find revenue by region
print("\n===== SALES BY REGION =====")
region_sales = df.groupby("Region")["TotalSales"].sum()
print(region_sales.sort_values(ascending=False))

# 5. Find the product with the highest revenue
print("\n===== TOP PRODUCT =====")
print(product_sales.idxmax())

# ===== BUSINESS INSIGHTS =====

print("\n===== REVENUE BY CATEGORY =====")
category_sales = df.groupby("Category")["TotalSales"].sum()
print(category_sales.sort_values(ascending=False))

print("\n===== QUANTITY SOLD BY PRODUCT =====")
product_quantity = df.groupby("Product")["Quantity"].sum()
print(product_quantity.sort_values(ascending=False))

print("\n===== TOP 3 ORDERS BY REVENUE =====")
top_orders = df.sort_values("TotalSales", ascending=False)
print(top_orders[["OrderID", "Product", "TotalSales"]].head(3))

# ===== DATA QUALITY CHECK =====

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())
import matplotlib.pyplot as plt

# Chart 1: Revenue by Product
plt.figure(figsize=(8, 5))
product_sales.sort_values().plot(kind="bar", color="skyblue")

plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("product_sales.png")
plt.show()

# Chart 2: Revenue by Region
plt.figure(figsize=(8, 5))
region_sales.sort_values().plot(kind="bar", color="orange")

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("region_sales.png")
plt.show()

print("\nCharts saved successfully!")

# ===== MONTHLY REVENUE LINE CHART =====

plt.figure(figsize=(9, 5))

monthly_sales.plot(
    kind="line",
    marker="o",
    linewidth=2
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("monthly_sales_trend.png")
plt.show()

print("\nMonthly revenue chart saved successfully!")

# ===== SALES PERFORMANCE SUMMARY =====

total_revenue = df["TotalSales"].sum()
total_orders = df["OrderID"].nunique()
total_units = df["Quantity"].sum()

average_order_value = total_revenue / total_orders

product_sales = df.groupby("Product")["TotalSales"].sum()
region_sales = df.groupby("Region")["TotalSales"].sum()

best_product = product_sales.idxmax()
best_region = region_sales.idxmax()

print("\n===== SALES PERFORMANCE SUMMARY =====")
print(f"Total Revenue: Rs. {total_revenue:,.2f}")
print(f"Total Orders: {total_orders}")
print(f"Total Units Sold: {total_units}")
print(f"Average Revenue per Order: Rs. {average_order_value:,.2f}")
print(f"Best Performing Product: {best_product}")
print(f"Best Performing Region: {best_region}")