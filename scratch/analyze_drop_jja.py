import pandas as pd
import json

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
items_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_items_dataset_202604222030.csv"
payments_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"
products_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_products_dataset_202604222030.csv"
customers_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
items = pd.read_csv(items_p)
payments = pd.read_csv(payments_p)
products = pd.read_csv(products_p)
customers = pd.read_csv(customers_p)

# Filter June, July, August 2018
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
df_jja = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month.isin([6, 7, 8]))].copy()

# Merges
merged = pd.merge(df_jja, items, on='order_id')
merged = pd.merge(merged, products, on='product_id')
merged = pd.merge(merged, customers, on='customer_id')
merged = pd.merge(merged, payments, on='order_id')

# Analysis by Month and Category
merged['month'] = merged['order_purchase_timestamp'].dt.month
summary = merged.groupby(['month', 'product_category_name']).agg({
    'order_id': 'nunique',
    'payment_value': 'sum'
}).reset_index()

summary['ticket_medio'] = summary['payment_value'] / summary['order_id']

# Top 10 categories overall in JJA
top_cats = summary.groupby('product_category_name')['payment_value'].sum().sort_values(ascending=False).head(10).index

# Prepare chart data
data_json = {
    "months": ["Junho", "Julho", "Agosto"],
    "categories": top_cats.tolist(),
    "volumes": {},
    "revenues": {},
    "tickets": {}
}

for cat in top_cats:
    cat_data = summary[summary['product_category_name'] == cat]
    data_json["volumes"][cat] = [int(cat_data[cat_data['month'] == m]['order_id'].values[0]) if m in cat_data['month'].values else 0 for m in [6, 7, 8]]
    data_json["revenues"][cat] = [float(cat_data[cat_data['month'] == m]['payment_value'].values[0]) if m in cat_data['month'].values else 0 for m in [6, 7, 8]]
    data_json["tickets"][cat] = [float(cat_data[cat_data['month'] == m]['ticket_medio'].values[0]) if m in cat_data['month'].values else 0 for m in [6, 7, 8]]

with open('scratch/drop_jja_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/drop_jja_data.json")
