import streamlit as st
import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#   DATABASE FUNCTION
def get_sales_data(category, sub_category, product):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="palak@Thakur8699",
        database="saless_db"
    )

    if category == "clothes":
        query = """
        select date, quantity
        from sales
        where category=%s and sub_category=%s and product=%s
        order by date
        """
        df = pd.read_sql(query, con, params=(category, sub_category, product))
    else:
        query = """
        select date, quantity
        from sales
        where category=%s and sub_category='none' and product=%s
        order by date
        """
        df = pd.read_sql(query, con, params=(category, product))

    con.close()
    return df



#  PREDICTION FUNCTIONS
def weekly_prediction(qty):
    return int(np.mean(qty[-4:]))

def monthly_prediction(qty):
    return int(np.mean(qty[-12:]))

def trend_based_prediction(qty, days):
    if len(qty) < 2:
        return [qty[-1]] * days

    trend = qty[-1] - qty[-2]
    future = []

    last_value = qty[-1]
    for i in range(days):
        next_value = last_value + trend
        future.append(max(0, next_value))  # avoid negative sales
        last_value = next_value

    return future



#  STREAMLIT UI 
st.set_page_config(page_title="Sales Prediction Dashboard", layout="wide")

st.title("📊 𝑺𝒂𝒍𝒆𝒔 𝑷𝒓𝒆𝒅𝒊𝒄𝒕𝒊𝒐𝒏 𝑫𝒂𝒔𝒉𝒃𝒐𝒂𝒓𝒅")
st.write("Predict weekly and monthly sales using historical data")

#  SIDEBAR
st.sidebar.header("🔍 Select Options")

category = st.sidebar.selectbox(
    "Select Category",
    ["electronics", "stationary", "supermarket", "clothes"]
)

sub_category = "none"
if category == "clothes":
    sub_category = st.sidebar.selectbox("Select Gender", ["men", "women"])

products = {
    "electronics": ["laptop", "smartwatch", "headphones", "mobile"],
    "stationary": ["pen", "pencil", "notebook", "page-folder"],
    "supermarket": ["rice", "cooking oil", "bread", "tea"],
    "clothes": {
        "men": ["shirt", "trouser"],
        "women": ["suits", "top"]
    }
}

if category == "clothes":
    product = st.sidebar.selectbox("Select Product", products["clothes"][sub_category])
else:
    product = st.sidebar.selectbox("Select Product", products[category])

prediction_type = st.sidebar.radio("Prediction Type", ["Weekly", "Monthly"])

#BUTTON 
if st.sidebar.button("🔮 Predict Sales"):

    #  Fetch data
    data = get_sales_data(category, sub_category, product)

    #  Check if data exists
    if data.empty:
        st.error("No data available for selected option")

    else:
        #  Historical quantities
        qty = data["quantity"].to_numpy()

#  Decide future days
        future_days = 4 if prediction_type == "Weekly" else 12

        #  Trend-based future prediction
        future_qty = trend_based_prediction(qty, future_days)

        #  Display prediction number
        if prediction_type == "Weekly":
            prediction = weekly_prediction(qty)
        else:
            prediction = monthly_prediction(qty)

        st.success(f" Predicted {prediction_type} Sales: **{prediction} units**")

        #  Combine past + future for graph
        data["date"] = pd.to_datetime(data["date"])
        past_dates = data["date"].tolist()
        last_date = data["date"].iloc[-1]

        if prediction_type == "Weekly":
              future_dates = pd.date_range(
        start=last_date + pd.Timedelta(weeks=1),
        periods=future_days,
        freq="W"
    )
        else:
         future_dates = pd.date_range(
        start=last_date + pd.DateOffset(months=1),
        periods=future_days,
        freq="M"
    )


        all_dates = list(past_dates) + list(future_dates)

        all_qty = list(qty) + future_qty

           
           #  Plot graph (Bold future prediction)
    st.subheader("📊 Historical vs Future Sales")

    fig, ax = plt.subplots(figsize=(10, 5))

# Historical sales → bars
    ax.bar(
    data["date"],
    qty,
    label="Historical Sales",
    alpha=0.7
)

# Future dates
    last_date = pd.to_datetime(data["date"].iloc[-1])
    future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=future_days
)

# Future prediction → BOLD LINE
    ax.plot(
    future_dates,
    future_qty,
    marker="*",
    linewidth=4,       #  MAKES LINE BOLD
    markersize=4,      #  BIG DOTS
    linestyle="-",
    color="purple",
    label="Future Prediction"
)

    ax.set_xlabel("Date")
    ax.set_ylabel("Quantity Sold")
    ax.set_title("Sales Prediction (Future Highlighted)")
    ax.legend()
    plt.xticks(rotation=45)

    st.pyplot(fig)