import pandas as pd
import json

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
customers_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
customers = pd.read_csv(customers_p)

# Merge orders with customers to get unique_id
df = pd.merge(orders, customers, on='customer_id')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Sort by date to identify first purchase
df = df.sort_values(by='order_purchase_timestamp')

# Identify New vs Recurring
# A customer is "New" if it's their first order ever in the dataset.
# A customer is "Recurring" if they have at least one previous order.
df['order_rank'] = df.groupby('customer_unique_id').cumcount() + 1
df['customer_type'] = df['order_rank'].apply(lambda x: 'New' if x == 1 else 'Recurring')

# Filter 2018 (up to August, as per dataset limits)
df_2018 = df[df['order_purchase_timestamp'].dt.year == 2018].copy()
df_2018['month_num'] = df_2018['order_purchase_timestamp'].dt.month

# Group by Month and Type
summary = df_2018.groupby(['month_num', 'customer_type']).size().reset_index(name='count')

# Months list
months_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago"]
months_nums = list(range(1, 9))

new_counts = []
rec_counts = []

for m in months_nums:
    new_counts.append(int(summary[(summary['month_num'] == m) & (summary['customer_type'] == 'New')]['count'].values[0]) if not summary[(summary['month_num'] == m) & (summary['customer_type'] == 'New')].empty else 0)
    rec_counts.append(int(summary[(summary['month_num'] == m) & (summary['customer_type'] == 'Recurring')]['count'].values[0]) if not summary[(summary['month_num'] == m) & (summary['customer_type'] == 'Recurring')].empty else 0)

# Prepare JSON
data_json = {
    "labels": months_labels,
    "new_customers": new_counts,
    "recurring_customers": rec_counts
}

with open('scratch/retention_data.json', 'w') as f:
    json.dump(data_json, f)

print("Data exported to scratch/retention_data.json")
