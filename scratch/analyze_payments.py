import pandas as pd
import json

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
payments_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
payments = pd.read_csv(payments_p)

# Dates
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
df_full = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month.isin([3, 4, 5, 6, 7, 8]))].copy()

# Merge
merged = pd.merge(df_full, payments, on='order_id')
merged['month'] = merged['order_purchase_timestamp'].dt.month

# Group by Month and Payment Type
summary = merged.groupby(['month', 'payment_type']).agg({
    'order_id': 'nunique',
    'payment_value': 'sum',
    'payment_installments': 'mean'
}).reset_index()

# Calculate % Share per Month
summary['vol_share'] = summary.groupby('month')['order_id'].transform(lambda x: (x / x.sum()) * 100)

# Period Comparison (Mar-May vs Jun-Aug)
p1 = summary[summary['month'].isin([3, 4, 5])].groupby('payment_type').agg({'order_id': 'sum', 'payment_value': 'sum'}).reset_index()
p2 = summary[summary['month'].isin([6, 7, 8])].groupby('payment_type').agg({'order_id': 'sum', 'payment_value': 'sum'}).reset_index()

p1['share'] = (p1['order_id'] / p1['order_id'].sum()) * 100
p2['share'] = (p2['order_id'] / p2['order_id'].sum()) * 100

# Prepare JSON
data_json = {
    "months": ["Março", "Abril", "Maio", "Junho", "Julho", "Agosto"],
    "payment_types": summary['payment_type'].unique().tolist(),
    "monthly_data": {},
    "comparison": {
        "p1": p1.to_dict(orient='records'),
        "p2": p2.to_dict(orient='records')
    }
}

for pt in data_json['payment_types']:
    pt_data = summary[summary['payment_type'] == pt]
    data_json["monthly_data"][pt] = [float(pt_data[pt_data['month'] == m]['vol_share'].values[0]) if m in pt_data['month'].values else 0 for m in [3, 4, 5, 6, 7, 8]]

with open('scratch/payment_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/payment_data.json")
