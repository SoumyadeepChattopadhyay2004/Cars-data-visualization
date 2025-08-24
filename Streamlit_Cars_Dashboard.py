import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Cars Datasets 2025.csv", encoding="latin1")

st.title("Cars Dataset 2025 - Data Visualization Dashboard")

# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Sidebar filters
st.sidebar.header("Filters")
selected_company = st.sidebar.multiselect("Select Company", df["Company Names"].unique())
selected_fuel = st.sidebar.multiselect("Select Fuel Type", df["Fuel Types"].unique())

filtered_df = df.copy()
if selected_company:
    filtered_df = filtered_df[filtered_df["Company Names"].isin(selected_company)]
if selected_fuel:
    filtered_df = filtered_df[filtered_df["Fuel Types"].isin(selected_fuel)]

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Visualization 1: Cars by Company
st.subheader("Number of Cars by Company")
company_counts = filtered_df["Company Names"].value_counts()
fig, ax = plt.subplots()
company_counts.plot(kind="bar", ax=ax)
ax.set_ylabel("Number of Cars")
st.pyplot(fig)

# Visualization 2: Fuel Type Distribution
import plotly.express as px
st.subheader("Fuel Type Distribution")
fuel_counts = filtered_df["Fuel Types"].value_counts().reset_index()
fuel_counts.columns = ["Fuel Type", "Count"]

fig2 = px.pie(
    fuel_counts,
    values="Count",
    names="Fuel Type",
    title="Fuel Type Share",
    hole=0.3  
)
fig2.update_traces(textinfo="percent+label", pull=[0.05]*len(fuel_counts))  
st.plotly_chart(fig2)

# Helper: Extract numeric horsepower values
def parse_hp(hp):
    try:
        if "-" in str(hp):
            return int(hp.split("-")[1].split()[0])
        else:
            return int(str(hp).split()[0])
    except:
        return None

# Helper: Extract numeric price (handle ranges, $ and commas)
def parse_price(price):
    try:
        p = str(price).replace("$", "").replace(",", "")
        if "-" in p:
            return int(p.split("-")[1])
        return int(p)
    except:
        return None

# Add numeric columns
filtered_df["HorsePower_num"] = filtered_df["HorsePower"].apply(parse_hp)
filtered_df["Price_num"] = filtered_df["Cars Prices"].apply(parse_price)

# Visualization 3: Horsepower Distribution
st.subheader("Horsepower Distribution")
fig3, ax3 = plt.subplots()
ax3.hist(filtered_df["HorsePower_num"].dropna(), bins=20, color='skyblue', edgecolor='black')
ax3.set_xlabel("HorsePower (hp)")
ax3.set_ylabel("Number of Cars")
st.pyplot(fig3)

# Visualization 4: Price vs Horsepower
st.subheader("Price vs HorsePower")
fig4, ax4 = plt.subplots()
ax4.scatter(filtered_df["HorsePower_num"], filtered_df["Price_num"], alpha=0.6)
ax4.set_xlabel("HorsePower (hp)")
ax4.set_ylabel("Price ($)")
st.pyplot(fig4)

# Visualization 5: Top 10 Most Expensive Cars
st.subheader("Top 10 Most Expensive Cars")
top_cars = filtered_df.dropna(subset=["Price_num"]).nlargest(10, "Price_num")
fig5, ax5 = plt.subplots()
ax5.barh(top_cars["Cars Names"], top_cars["Price_num"], color="orange")
ax5.set_xlabel("Price ($)")
ax5.invert_yaxis()
st.pyplot(fig5)

# Visualization 6: Seats Distribution
st.subheader("Seats Distribution")
seat_counts = filtered_df["Seats"].value_counts()
fig6, ax6 = plt.subplots()
seat_counts.plot(kind="bar", ax=ax6, color="green")
ax6.set_ylabel("Number of Cars")
st.pyplot(fig6)

# Visualization 7: Average Price by Fuel Type 
st.subheader("Average Price by Fuel Type")
avg_prices = filtered_df.groupby("Fuel Types")["Price_num"].mean().dropna()
fig7, ax7 = plt.subplots()
avg_prices.plot(kind="line", marker="o", ax=ax7, color="purple")
ax7.set_ylabel("Average Price ($)")
ax7.set_xlabel("Fuel Type")
st.pyplot(fig7)

# Visualization 8: 0–100 km/h Acceleration vs HorsePower
st.subheader("Acceleration (0-100 km/h) vs HorsePower")
def parse_acceleration(x):
    try:
        return float(str(x).replace("sec", "").strip())
    except:
        return None

filtered_df["Acceleration"] = filtered_df["Performance(0 - 100 )KM/H"].apply(parse_acceleration)

fig8, ax8 = plt.subplots()
ax8.scatter(filtered_df["HorsePower_num"], filtered_df["Acceleration"], c="red", alpha=0.6)
ax8.set_xlabel("HorsePower (hp)")
ax8.set_ylabel("0-100 km/h (seconds)")
ax8.invert_yaxis()  # Faster cars (lower seconds) appear higher
st.pyplot(fig8)
