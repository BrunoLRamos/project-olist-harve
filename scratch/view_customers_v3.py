import csv
from collections import Counter

file_path = '/Users/brunoramos/Documents/Pessoais/Projetos/project-olist-harve/tabelas/olist_customers_dataset_202604222030.csv'

def print_table(data, limit=15):
    if not data:
        return
    
    widths = [0] * len(data[0])
    for row in data[:limit]:
        for i, val in enumerate(row):
            widths[i] = max(widths[i], len(str(val)))
            
    header = data[0]
    print(" | ".join(val.ljust(widths[i]) for i, val in enumerate(header)))
    print("-|-".join("-" * widths[i] for i in range(len(widths))))
    
    for row in data[1:limit]:
        print(" | ".join(str(val).ljust(widths[i]) for i, val in enumerate(row)))

try:
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
        
    print(f"Total de registros: {len(rows)}\n")
    
    print("--- Preview (Top 15) ---")
    print_table([header] + rows[:15])
    
    # Calculate some stats
    cities = [row[3] for row in rows]
    states = [row[4] for row in rows]
    
    top_cities = Counter(cities).most_common(5)
    top_states = Counter(states).most_common(5)
    
    print("\n--- Top 5 Cidades ---")
    for city, count in top_cities:
        print(f"{city}: {count}")
        
    print("\n--- Top 5 Estados ---")
    for state, count in top_states:
        print(f"{state}: {count}")
    
except Exception as e:
    print(f"Erro: {e}")
