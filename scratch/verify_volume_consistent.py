import pandas as pd
df = pd.read_csv("/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv")
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df_2018 = df[df['order_purchase_timestamp'].dt.year == 2018]
p1 = df_2018[(df_2018['order_purchase_timestamp'].dt.month >= 3) & (df_2018['order_purchase_timestamp'].dt.month <= 5)]
p2 = df_2018[(df_2018['order_purchase_timestamp'].dt.month >= 6) & (df_2018['order_purchase_timestamp'].dt.month <= 8)]
print(f"Volume P1: {len(p1)}")
print(f"Volume P2: {len(p2)}")
