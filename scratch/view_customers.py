import pandas as pd
import sys

file_path = '/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv'

try:
    df = pd.read_csv(file_path)
    
    # Basic info
    print(f"Total de registros: {len(df)}")
    print(f"Cidades únicas: {df['customer_city'].nunique()}")
    print(f"Estados únicos: {df['customer_state'].nunique()}")
    print("\n--- Preview (Top 10) ---\n")
    print(df.head(10).to_markdown(index=False))
    
    # Summary by state
    print("\n--- Top 5 Estados ---\n")
    print(df['customer_state'].value_counts().head(5).to_markdown())

except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
