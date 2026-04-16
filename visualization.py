import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


def fetch_sales(category, sub_category, product):
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="palak@Thakur8699",
        database="saless_db"
    )

    query = """
    select date, quantity
    from sales
    where category=%s and sub_category=%s and product=%s
    order by date
    """

    df = pd.read_sql(query, con, params=(category, sub_category, product))
    con.close()
    return df


if __name__ == "__main__":
    data = fetch_sales(
        category="electronics",
        sub_category="none",
        product="laptop"
    )

    plt.figure()
    plt.bar(data["date"], data["quantity"])
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.title("Sales Comparison (Bar Graph)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
