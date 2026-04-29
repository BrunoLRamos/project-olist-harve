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

# Filter Mar-Aug 2018
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
df_full = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month.isin([3, 4, 5, 6, 7, 8]))].copy()

# Merges
merged = pd.merge(df_full, items, on='order_id')
merged = pd.merge(merged, products, on='product_id')

# Aggregation: Category Volume
merged['month'] = merged['order_purchase_timestamp'].dt.month
summary = merged.groupby(['month', 'product_category_name']).size().reset_index(name='volume')

# Top 10 categories overall in these months
top_cats = merged.groupby('product_category_name').size().sort_values(ascending=False).head(10).index

# Prepare chart data
data_json = {
    "months": ["Março", "Abril", "Maio", "Junho", "Julho", "Agosto"],
    "categories": top_cats.tolist(),
    "volumes": {}
}

for cat in top_cats:
    cat_data = summary[summary['product_category_name'] == cat]
    data_json["volumes"][cat] = [int(cat_data[cat_data['month'] == m]['volume'].values[0]) if m in cat_data['month'].values else 0 for m in [3, 4, 5, 6, 7, 8]]

with open('scratch/drop_full_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/drop_full_data.json")
