import pandas as pd

orders_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
payments_path = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"

df_orders = pd.read_csv(orders_path)
df_payments = pd.read_csv(payments_path)
df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])

# Filter 2018
df_2018 = df_orders[df_orders['order_purchase_timestamp'].dt.year == 2018].copy()
df_combined = pd.merge(df_2018, df_payments, on='order_id', how='inner')

# Period 1: Mar-Mai
p1 = df_combined[(df_combined['order_purchase_timestamp'].dt.month >= 3) & (df_combined['order_purchase_timestamp'].dt.month <= 5)]
val1 = p1['payment_value'].sum()
vol1 = p1['order_id'].nunique()

# Period 2: Jun-Ago
p2 = df_combined[(df_combined['order_purchase_timestamp'].dt.month >= 6) & (df_combined['order_purchase_timestamp'].dt.month <= 8)]
val2 = p2['payment_value'].sum()
vol2 = p2['order_id'].nunique()

retraction_val = ((val2 - val1) / val1) * 100

print(f"P1 (Mar-Mai): R$ {val1:,.2f} ({vol1} pedidos)")
print(f"P2 (Jun-Ago): R$ {val2:,.2f} ({vol2} pedidos)")
print(f"Retração Faturamento: {retraction_val:.2f}%")
