import pandas as pd
import json

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
items_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_items_dataset_202604222030.csv"
products_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_products_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
items = pd.read_csv(items_p)
products = pd.read_csv(products_p)

# Filter 2018
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
df_2018 = orders[orders['order_purchase_timestamp'].dt.year == 2018].copy()

# Merges
merged = pd.merge(df_2018, items, on='order_id')
merged = pd.merge(merged, products, on='product_id')

# Aggregation: Category Volume
cat_volume = merged.groupby('product_category_name').size().sort_values(ascending=False).head(20)

data_json = {
    "categories": cat_volume.index.tolist(),
    "values": cat_volume.values.tolist()
}

with open('scratch/cat_volume_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/cat_volume_data.json")
