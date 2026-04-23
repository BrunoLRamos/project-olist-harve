import pandas as pd
import os

tabelas_dir = 'tabelas'
output_dir = 'scratch'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

csv_files = [f for f in os.listdir(tabelas_dir) if f.endswith('.csv')]
previews = []

# Template HTML básico com Bootstrap para ficar bonito
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Olist Data Preview - {title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 20px; background-color: #f8f9fa; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        h1 {{ color: #0d6efd; margin-bottom: 20px; }}
        .table-container {{ overflow-x: auto; }}
        .nav-link {{ margin-right: 10px; }}
    </style>
</head>
<body>
    <div class="container-fluid">
        <nav class="navbar navbar-expand-lg navbar-light bg-light mb-4 rounded">
            <div class="container-fluid">
                <a class="navbar-brand" href="index.html">Olist Dashboard</a>
                <div class="navbar-nav">
                    {nav_links}
                </div>
            </div>
        </nav>
        <h1>{title}</h1>
        <p class="text-muted">Mostrando as primeiras 100 linhas de {filename}</p>
        <div class="table-container">
            {table_html}
        </div>
    </div>
</body>
</html>
"""

# Primeiro passo: Gerar os previews individuais
for csv in csv_files:
    table_name = csv.replace('.csv', '').replace('_dataset_202604222030', '')
    output_file = f"{table_name}_preview.html"
    
    print(f"Processando {table_name}...")
    
    try:
        df = pd.read_csv(os.path.join(tabelas_dir, csv))
        table_html = df.head(100).to_html(classes='table table-hover table-bordered table-sm')
        previews.append({'name': table_name, 'file': output_file})
    except Exception as e:
        print(f"Erro ao processar {csv}: {e}")

# Gerar os links de navegação
nav_links = "".join([f'<a class="nav-link" href="{p["file"]}">{p["name"].replace("olist_", "").capitalize()}</a>' for p in previews])

# Salvar cada página com a navegação incluída
for p in previews:
    # Re-processar para incluir os nav_links corretos
    df = pd.read_csv(os.path.join(tabelas_dir, csv_files[previews.index(p)]))
    table_html = df.head(100).to_html(classes='table table-hover table-bordered table-sm')
    
    full_html = html_template.format(
        title=p['name'].replace('_', ' ').title(),
        filename=csv_files[previews.index(p)],
        table_html=table_html,
        nav_links=nav_links
    )
    
    with open(os.path.join(output_dir, p['file']), 'w') as f:
        f.write(full_html)

# Criar a página index.html
index_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Olist Data Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding: 50px; background-color: #f4f7f6; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        .card {{ transition: transform 0.2s; border: none; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }}
        .card-title {{ color: #2c3e50; font-weight: bold; }}
        h1 {{ text-align: center; margin-bottom: 50px; color: #2c3e50; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Olist Data Dashboard</h1>
        <div class="row g-4">
            {"".join([f'''
            <div class="col-md-4">
                <div class="card h-100">
                    <div class="card-body text-center">
                        <h5 class="card-title">{p["name"].replace("olist_", "").replace("_", " ").title()}</h5>
                        <p class="card-text text-muted">Amostra de 100 linhas</p>
                        <a href="{p["file"]}" class="btn btn-primary">Visualizar Tabela</a>
                    </div>
                </div>
            </div>
            ''' for p in previews])}
        </div>
    </div>
</body>
</html>
"""

with open(os.path.join(output_dir, 'index.html'), 'w') as f:
    f.write(index_content)

print("\nDashboard gerado com sucesso em scratch/index.html")
