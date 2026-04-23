import csv

file_path = '/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv'

def print_table(data, limit=15):
    if not data:
        return
    
    # Calculate column widths
    widths = [0] * len(data[0])
    for row in data[:limit]:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
            
    # Print header
    header = data[0]
    sep = " | "
    print(" | ".join(val.ljust(widths[i]) for i, val in enumerate(header)))
    print("-|-".join("-" * widths[i] for i in range(len(widths))))
    
    # Print rows
    for row in data[1:limit]:
        print(" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)))

try:
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
    print(f"Total de registros: {len(rows) - 1}\n")
    print_table(rows)
    
except Exception as e:
    print(f"Erro: {e}")
