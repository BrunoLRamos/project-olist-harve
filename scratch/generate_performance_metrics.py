import pandas as pd
import json

# Caminhos
orders_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
payments_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"

# Carregar dados
df_orders = pd.read_csv(orders_path)
df_payments = pd.read_csv(payments_path)

# Converter datas
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])

# Filtrar 2018
df_orders_2018 = df_orders[df_orders['order_purchase_timestamp'].dt.year == 2018].copy()

# Join com pagamentos
df_combined = pd.merge(df_orders_2018, df_payments, on='order_id', how='inner')

# Agrupamento mensal
monthly_data = df_combined.groupby(df_combined['order_purchase_timestamp'].dt.month).agg({
    'order_id': 'nunique',
    'payment_value': 'sum'
}).reset_index()

month_map = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set'}
monthly_data['month_name'] = monthly_data['order_purchase_timestamp'].map(month_map)
monthly_data = monthly_data.dropna(subset=['month_name'])

# Preparar dados para JSON
labels = monthly_data['month_name'].tolist()
volumes = monthly_data['order_id'].tolist()
values = monthly_data['payment_value'].tolist()

print(json.dumps({"labels": labels, "volumes": volumes, "values": values}))
