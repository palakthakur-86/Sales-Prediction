import pandas as pd
import mysql.connector

df = pd.read_csv("extra_sales_data.csv")

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="palak@Thakur8699",
    database="saless_db"
)

c = con.cursor()

query = """
INSERT INTO sales (date, category, sub_category, product, price, quantity, total_sales)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    c.execute(query, tuple(row))

con.commit()
con.close()

print("Extra data added successfully (old data kept)")
