import pandas as pd

files = [
    "cleaned_clothes.csv",
    "cleaned_supermarket.csv",
    "cleaned_stationary.csv",
    "cleaned_electronic.csv" 
]

df = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

df.to_csv("master_sales_data.csv", index=False)

print("master_sales_data.csv created successfully")
