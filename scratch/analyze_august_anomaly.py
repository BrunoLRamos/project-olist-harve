import pandas as pd

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
items_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_items_dataset_202604222030.csv"
products_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_products_dataset_202604222030.csv"
payments_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
items = pd.read_csv(items_p)
products = pd.read_csv(products_p)
payments = pd.read_csv(payments_p)

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Filter Jul and Aug 2018
df_jul = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month == 7)]
df_aug = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month == 8)]

def get_stats(df, month_name):
    merged = pd.merge(df, items, on='order_id')
    merged = pd.merge(merged, products, on='product_id')
    
    pay_merged = pd.merge(df, payments, on='order_id')
    
    avg_ticket = pay_merged['payment_value'].sum() / df['order_id'].nunique()
    avg_price = merged['price'].mean()
    
    top_cats = merged['product_category_name'].value_counts().head(5)
    
    print(f"--- {month_name} ---")
    print(f"Volume: {df['order_id'].nunique()}")
    print(f"Faturamento Total: R$ {pay_merged['payment_value'].sum():,.2f}")
    print(f"Ticket Médio: R$ {avg_ticket:.2f}")
    print(f"Preço Médio Item: R$ {avg_price:.2f}")
    print(f"Top 5 Categorias:\n{top_cats}")
    print("\n")

get_stats(df_jul, "JULHO")
get_stats(df_aug, "AGOSTO")
