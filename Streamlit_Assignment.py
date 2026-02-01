import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.set_page_config(page_title="Ebay Laptop Sales Dashboard", layout="wide")

st.title("eBay Laptop Sales Dashboard")
st.write("This dashboard analyzes cleaned eBay laptop sales data and provides business insights.")


df = pd.read_csv("EbayCleanedDataSample.csv")

##st.write("Column names:", df.columns.tolist())

st.subheader(" Cleaned Dataset Preview")

st.dataframe(df)


st.header(" Filter Your Dataset")




brand_options = df["Brand"].dropna().unique()
selected_brands = st.multiselect("Filter by Brand", brand_options, default=brand_options)

condition_options = df["Condition"].dropna().unique()
selected_condition = st.selectbox("Select Condition", ["All"] + list(condition_options))

min_price, max_price = float(df["Price"].min()), float(df["Price"].max())
price_range = st.slider("Select Price Range ($)", min_price, max_price, (min_price, max_price))

filtered_df = df[df["Brand"].isin(selected_brands)]
filtered_df = filtered_df[(filtered_df["Price"] >= price_range[0]) & (filtered_df["Price"] <= price_range[1])]
if selected_condition != "All":
    filtered_df = filtered_df[filtered_df["Condition"] == selected_condition]

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)




st.header("Average Price by Laptop Brand (Streamlit Chart)")

avg_price_brand = filtered_df.groupby("Brand")["Price"].mean().sort_values()

st.bar_chart(avg_price_brand)

st.subheader("Business Analysis")
st.write("""
From a business perspective, brands with consistently higher average sale prices 
(such as Apple or high-end gaming laptops if present) represent premium market segments. 
These insights suggest which brands may warrant increased purchasing, marketing 
attention, or pricing review. Conversely, brands with low resale value may be ideal 
for bulk sourcing or discount promotions.
""")




st.header("Plotly Chart: Price by Brand")


if "Brand" in filtered_df.columns and "Price" in filtered_df.columns:

    price_fig = px.scatter(
        filtered_df,
        x="Brand",
        y="Price",
        color="Brand",
        title="Price by Laptop Brand",
        labels={"Brand": "Brand", "Price": "Price ($)"}
    )

    st.plotly_chart(price_fig)

else:
    st.error("Your dataset does not contain 'brand' and 'price' columns. Please check column names.")

    st.subheader("Business Analysis")
    st.write("""
Newer laptops predictably reflect higher resale prices, indicating strong demand 
for modern hardware features. Older laptops show greater price variability, 
suggesting that specs (RAM, CPU, SSD) drive value rather than age alone. 
This insight can guide purchasing decisions for used inventory.
""")





st.header(" Dynamic Plotly Chart: Price by Condition")

condition_for_chart = st.selectbox(
    "Choose Condition to Display",
    df["Condition"].unique()
)

condition_df = df[df["Condition"] == condition_for_chart]

cond_fig = px.box(
    condition_df,
    x="Brand",
    y="Price",
    title=f"Price Distribution by Brand ({condition_for_chart} Condition)",
    labels={"brand": "Laptop Brand", "price": "Price ($)"}
)

st.plotly_chart(cond_fig)