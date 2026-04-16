import pandas as pd
import mysql.connector

df = pd.read_csv("master_sales_data.csv")

import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="palak@Thakur8699",
    database="saless_db"
)

c = con.cursor()
# c.execute("create database if not exists saless_db")

# print("Database created successfully")

# c.execute("""
# create table if not exists sales (
#     id int auto_increment primary key,
#     date DATE,
#     category varchar(50),
#     sub_category varchar(50),
#     product varchar(100),
#     price float,
#     quantity int,
#     total_sales float
# )
# """)
 
# print("Table created successfully")


# query = """
# insert into sales (date, category, sub_category, product, price, quantity, total_sales)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# """

# for _, row in df.iterrows():
#     c.execute(query, tuple(row))

# con.commit()

# print("Data inserted successfully")

# c.execute("select * from sales limit 5")
# for i in c:
#     print(i)

# c.execute("""alter table sales add cost_price float, add selling_price float""")
#print("cost_price and selling_price columns added successfully")
c.execute("""update sales set selling_price = price, cost_price = price * 0.7 where cost_price is null""")

print(" Cost & Selling prices updated")
con.commit()
c.close()
# con.close()
