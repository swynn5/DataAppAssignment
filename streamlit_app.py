import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# 1 - Dropdown for Category using the specified format
# Section: Category Selection
st.write("### Category Selection")
category_selected = st.selectbox(
    "Select a Category",
    df["Category"].unique(),
    index=None,
    placeholder="Select a category..."
)

st.write("You selected:", category_selected)

# Filter data based on selected category
df_filtered = df[df["Category"] == category_selected]

# 2 - Multi-select for Sub_Category in the selected Category
# Section: Sub-Category Selection
st.write("### Sub-Category Selection")
subcategories_selected = st.multiselect("Select one or multiple sub-categories", df_filtered["Sub_Category"].unique())

# Filter data based on selected sub_categories
df_final = df_filtered[df_filtered["Sub_Category"].isin(subcategories_selected)]

# 3 - Line chart of sales for selected sub-categories
# Section: Sales Trend Visualization
st.write("### Sales Trend Visualization")
if not df_final.empty:
    df_final["Order_Date"] = pd.to_datetime(df_final["Order_Date"])
    df_final.set_index('Order_Date', inplace=True)
    sales_by_month_filtered = df_final.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered, y="Sales")

# (4) Calculate metrics for the selected items
# Section: Metrics Calculation
st.write("### Metrics Calculation")
if not df_final.empty:
    total_sales = df_final["Sales"].sum()
    total_profit = df_final["Profit"].sum()
    overall_profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # Calculate overall profit margin for all products across all categories
    total_sales_all = df["Sales"].sum()
    total_profit_all = df["Profit"].sum()
    overall_profit_margin_all = (total_profit_all / total_sales_all) * 100 if total_sales_all > 0 else 0
    delta_profit_margin = overall_profit_margin - overall_profit_margin_all

    # (5) Display metrics with delta
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Overall Profit Margin (%)", value=f"{overall_profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")

# Section: Overall Sales Visualization
st.write("### Overall Sales Visualization")
# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")
