import pandas as pd

# Caminhos
orders_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_orders_dataset_202604222030.csv"
items_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_items_dataset_202604222030.csv"
payments_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_order_payments_dataset_202604222030.csv"
products_p = "/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_products_dataset_202604222030.csv"

# Load
orders = pd.read_csv(orders_p)
items = pd.read_csv(items_p)
payments = pd.read_csv(payments_p)
products = pd.read_csv(products_p)

# Dates
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Period 1: Mar, Apr, May 2018
p1 = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month.isin([3, 4, 5]))]
# Period 2: Jun, Jul, Aug 2018
p2 = orders[(orders['order_purchase_timestamp'].dt.year == 2018) & (orders['order_purchase_timestamp'].dt.month.isin([6, 7, 8]))]

def get_rev_by_cat(df):
    merged = pd.merge(df, items, on='order_id')
    merged = pd.merge(merged, products, on='product_id')
    merged = pd.merge(merged, payments, on='order_id')
    return merged.groupby('product_category_name')['payment_value'].sum()

rev_p1 = get_rev_by_cat(p1)
rev_p2 = get_rev_by_cat(p2)

# Delta
comparison = pd.DataFrame({'P1': rev_p1, 'P2': rev_p2}).fillna(0)
comparison['delta'] = comparison['P2'] - comparison['P1']
comparison['pct_change'] = (comparison['delta'] / comparison['P1']) * 100

print("--- Categorias com MAIOR QUEDA em R$ ---")
print(comparison.sort_values(by='delta').head(5))

print("\n--- Categorias com MAIOR QUEDA em % (min R$ 50k em P1) ---")
print(comparison[comparison['P1'] > 50000].sort_values(by='pct_change').head(5))
