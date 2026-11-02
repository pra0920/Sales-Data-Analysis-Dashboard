# 📊 Sales Data Analysis Dashboard

## Project Overview

This project analyzes sales data using Python and builds an interactive dashboard with Streamlit. It helps explore revenue, product performance, regional sales, monthly trends, and business insights.

**Project Type:** Data Analysis & Interactive Dashboard  
**Language:** Python  
**Dataset:** Sample sales data created for learning purposes

## Features

- Interactive sales dashboard
- KPI metrics: Total Revenue, Total Orders, Units Sold, and Average Order Value
- Product and region filters
- Date range filter
- Monthly revenue trend analysis
- Revenue by product and region
- Product performance analytics
- Automated business insights
- Month-over-month sales growth analysis
- Data quality checks for missing values and duplicates
- Downloadable monthly sales report
- Interactive charts using Plotly
- Sales data table and CSV download

## Technologies Used

- Python
- Pandas
- Matplotlib
- Plotly
- Streamlit
- Scikit-learn
- Visual Studio Code
- GitHub

## Project Files

- `dashboard.py` — Interactive Streamlit dashboard
- `main.py` — Main sales data analysis script
- `analysis.py` — Additional analysis
- `sales_large.csv` — Dataset used by the dashboard
- `sales.csv` — Sample sales dataset
- `requirements.txt` — Required Python libraries

## How to Run the Project

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Open the project folder

Open `Sales_Data_Analysis` in VS Code.

### 3. Install the required libraries

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your browser.

### 5. Run the main analysis script

```bash
python main.py
```

## Skills Demonstrated

- Reading and working with CSV files
- Data cleaning and quality checks
- Creating calculated columns
- Grouping and aggregating data
- Sorting and filtering datasets
- Exploratory Data Analysis (EDA)
- Data visualization
- Building interactive dashboards
- Extracting business insights
- Basic machine learning concepts

## Forecasting Note

A sales forecasting feature was explored using Linear Regression. The current dataset covers January to April 2026, so it does not contain enough historical data for the project's original forecasting requirement. Forecasting is therefore not currently included in the active dashboard.

## Future Improvements

- Use a larger real-world dataset
- Add more historical data for forecasting
- Improve dashboard design and usability
- Deploy the dashboard online
- Add more advanced analytical features

---

Created as a Data Science portfolio project using Python.
