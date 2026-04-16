import mysql.connector
import pandas as pd
import numpy as np


# ---------------- DATABASE CLASS ----------------
class Database:
    def get_sales_data(self, category, sub_category, product):
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="palak@Thakur8699",
            database="saless_db"
        )

        # Stationary has no sub_category
        if category == "stationary":
            query = """
            select date, quantity
            from sales
            where category = %s and product = %s
            order by date
            """
            df = pd.read_sql(query, con, params=(category, product))
        else:
            query = """
            select date, quantity
            from sales
            where category = %s and sub_category = %s and product = %s
            order by date
            """
            df = pd.read_sql(query, con, params=(category, sub_category, product))

        con.close()
        return df


# ---------------- PREDICTION CLASS (NO ML) ----------------
class SalesPredictor:

    # Weekly = average of last 4 records
    def weekly_prediction(self, quantities):
        if len(quantities) < 4:
            return int(np.mean(quantities))
        return int(np.mean(quantities[-4:]))

    # Monthly = average of last 12 records
    def monthly_prediction(self, quantities):
        if len(quantities) < 12:
            return int(np.mean(quantities))
        return int(np.mean(quantities[-12:]))

    # Future prediction = trend-based logic
    def future_prediction(self, quantities, days_ahead=1):
        if len(quantities) < 2:
            return int(quantities[-1])

        # Calculate trend
        trend = quantities[-1] - quantities[-2]

        # Predict future value
        future_value = quantities[-1] + (trend * days_ahead)

        return max(0, int(future_value))  # avoid negative sales


# ---------------- MAIN ----------------
if __name__ == "__main__":
    db = Database()
    predictor = SalesPredictor()

    data = db.get_sales_data(
        category="clothes",
        sub_category="men",
        product="shirt"
    )

    if data.empty:
        print("No data found")
        exit()

    quantities = data["quantity"].to_numpy()

    weekly = predictor.weekly_prediction(quantities)
    monthly = predictor.monthly_prediction(quantities)
    future = predictor.future_prediction(quantities, days_ahead=7)

    print("Weekly Sales Prediction:", weekly)
    print("Monthly Sales Prediction:", monthly)
    print("Future Sales Prediction:", future)
