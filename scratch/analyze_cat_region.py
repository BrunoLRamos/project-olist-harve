import pandas as pd
import json

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
items_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_items_dataset_202604222030.csv"
products_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_products_dataset_202604222030.csv"
customers_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
items = pd.read_csv(items_p)
products = pd.read_csv(products_p)
customers = pd.read_csv(customers_p)

# Filter 2018
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
df_2018 = orders[orders['order_purchase_timestamp'].dt.year == 2018].copy()

# Merges
merged = pd.merge(df_2018, items, on='order_id')
merged = pd.merge(merged, products, on='product_id')
merged = pd.merge(merged, customers, on='customer_id')

# Aggregation: Category vs State
pivot = merged.groupby(['product_category_name', 'customer_state']).size().unstack(fill_value=0)

# Select Top 10 Categories by total volume
top_cats = pivot.sum(axis=1).sort_values(ascending=False).head(10).index
pivot_top = pivot.loc[top_cats]

# Sort states by total volume in these categories
top_states = pivot_top.sum(axis=0).sort_values(ascending=False).index
pivot_final = pivot_top[top_states]

# Export data for Chart.js Heatmap or Stacked Bar
# Let's use a Stacked Bar: Categories as X-axis, States as stacks
data_json = {
    "categories": pivot_final.index.tolist(),
    "states": pivot_final.columns.tolist(),
    "values": pivot_final.values.tolist()
}

with open('scratch/cat_region_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/cat_region_data.json")
