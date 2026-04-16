import pandas as pd
import random
from datetime import datetime, timedelta

rows = []
start_date = datetime(2025, 1, 1)

categories = {
    "clothes": {
        "men": ["shirt", "trouser"],
        "women": ["suits", "top"]
    },
    "stationary": {
        "none": ["pen", "pencil", "notebook", "page-folder"]
    },
    "electronics": {
        "none": ["laptop", "mobile", "headphones", "smartwatch"]
    },
    "supermarket": {
        "none": ["rice", "cooking oil", "bread", "tea"]
    }
}

for i in range(35000):   # 👈 ADD ONLY (you can change count)
    category = random.choice(list(categories.keys()))
    sub_category = random.choice(list(categories[category].keys()))
    product = random.choice(categories[category][sub_category])

    date = start_date + timedelta(days=random.randint(0, 365))
    price = random.randint(10, 60000)
    quantity = random.randint(1, 40)
    total_sales = price * quantity

    rows.append([
        date.strftime("%Y-%m-%d"),
        category,
        sub_category,
        product,
        price,
        quantity,
        total_sales
    ])

df = pd.DataFrame(rows, columns=[
    "date", "category", "sub_category",
    "product", "price", "quantity", "total_sales"
])

# 👇 IMPORTANT: new file, NOT replacing old one
df.to_csv("extra_sales_data.csv", index=False)

print("✅ Extra sales data generated")