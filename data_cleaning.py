import pandas as pd

class DataCleaner:
    def clean_file(self, input_file, category, output_file):
        # read csv
        df = pd.read_csv(input_file)

        # rename columns to common names
        df.rename(columns={
            'sale_date': 'date',
            'product_name': 'product'
        }, inplace=True)

        # convert date column
        df['date'] = pd.to_datetime(df['date'])

        # add category column
        df['category'] = category.lower()

        # handle clothes gender as sub_category
        if 'gender' in df.columns:
            df['sub_category'] = df['gender'].str.lower().str.strip()
            df.drop(columns=['gender'], inplace=True)
        else:
            df['sub_category'] = 'none'

        # clean text data
        df['product'] = df['product'].str.lower().str.strip()

        # remove duplicates
        df.drop_duplicates(inplace=True)

        # remove invalid values
        df = df[df['quantity'] > 0]
        df = df[df['price'] > 0]

        # reorder columns
        df = df[['date', 'category', 'sub_category', 'product', 'price', 'quantity', 'total_sales']]

        # save cleaned csv
        df.to_csv(output_file, index=False)

        print(f"{output_file} created successfully")


# ---------- RUN CLEANING ----------
if __name__ == "__main__":
    cleaner = DataCleaner()

    cleaner.clean_file("clothe.csv", "clothe", "cleaned_clothe.csv")
    cleaner.clean_file("supermarket.csv", "supermarket", "cleaned_supermarket.csv")
    cleaner.clean_file("statioanry.csv", "statioanry", "cleaned_statioanry.csv")
    cleaner.clean_file("electronic.csv", "electronics", "cleaned_electronic.csv")
